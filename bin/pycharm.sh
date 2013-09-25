#!/bin/sh
#
# ---------------------------------------------------------------------
# PyCharm startup script.
# ---------------------------------------------------------------------
#

OS_TYPE="`uname -s`"

# ---------------------------------------------------------------------
# Locate a JDK installation directory which will be used to run the IDE.
# Try (in order): PYCHARM_JDK, JDK_HOME, JAVA_HOME, "java" in PATH.
# ---------------------------------------------------------------------
if [ -n "$PYCHARM_JDK" -a -x "$PYCHARM_JDK/bin/java" ]; then
  JDK="$PYCHARM_JDK"
elif [ -n "$JDK_HOME" -a -x "$JDK_HOME/bin/java" ]; then
  JDK="$JDK_HOME"
elif [ -n "$JAVA_HOME" -a -x "$JAVA_HOME/bin/java" ]; then
  JDK="$JAVA_HOME"
else
  JAVA_BIN_PATH=`which java`
  if [ -n "$JAVA_BIN_PATH" ]; then
    if [ "$OS_TYPE" = "FreeBSD" ]; then
      JAVA_LOCATION=`JAVAVM_DRYRUN=yes java | grep '^JAVA_HOME' | cut -c11-`
      if [ -x "$JAVA_LOCATION/bin/java" ]; then
        JDK="$JAVA_LOCATION"
      fi
    elif [ "$OS_TYPE" = "SunOS" ]; then
      JAVA_LOCATION="/usr/jdk/latest"
      if [ -x "$JAVA_LOCATION/bin/java" ]; then
        JDK="$JAVA_LOCATION"
      fi
    elif [ "$OS_TYPE" = "Darwin" ]; then
      JAVA_LOCATION=`/usr/libexec/java_home`
      if [ -x "$JAVA_LOCATION/bin/java" ]; then
        JDK="$JAVA_LOCATION"
      fi
    fi

    if [ -z "$JDK" -a -x "/bin/readlink" ]; then
      JAVA_LOCATION=`readlink -f "$JAVA_BIN_PATH"`
      case "$JAVA_LOCATION" in
        */jre/bin/java)
          JAVA_LOCATION=`echo "$JAVA_LOCATION" | xargs dirname | xargs dirname | xargs dirname` ;;
        *)
          JAVA_LOCATION=`echo "$JAVA_LOCATION" | xargs dirname | xargs dirname` ;;
      esac
      if [ -x "$JAVA_LOCATION/bin/java" ]; then
        JDK="$JAVA_LOCATION"
      fi
    fi
  fi
fi

if [ -z "$JDK" ]; then
  echo "ERROR: cannot start PyCharm."
  echo "No JDK found. Please validate either PYCHARM_JDK, JDK_HOME or JAVA_HOME environment variable points to valid JDK installation."
  echo
  echo "Press Enter to continue."
  read IGNORE
  exit 1
fi

VERSION_LOG=`mktemp -t java.version.log.XXXXXX`
$JDK/bin/java -version 2> "$VERSION_LOG"
grep 'OpenJDK' "$VERSION_LOG"
OPEN_JDK=$?
grep "64-Bit\|x86_64" "$VERSION_LOG"
BITS=$?
rm "$VERSION_LOG"
if [ $OPEN_JDK -eq 0 ]; then
  echo "WARNING: You are launching the IDE using OpenJDK Java runtime."
  echo
  echo "         ITS KNOWN TO HAVE PERFORMANCE AND GRAPHICS ISSUES!"
  echo "         SWITCH TO THE ORACLE(SUN) JDK BEFORE REPORTING PROBLEMS!"
  echo
  echo "NOTE:    If you have both Oracle (Sun) JDK and OpenJDK installed"
  echo "         please validate either PYCHARM_JDK, JDK_HOME, or JAVA_HOME environment variable points to valid Oracle (Sun) JDK installation."
  echo "         See http://ow.ly/6TuKQ for more info on switching default JDK."
  echo
  echo "Press Enter to continue."
# ---------------------------------------------------------------------
# COMMENT LINE BELOW TO REMOVE PAUSE AFTER OPEN JDK WARNING
# ---------------------------------------------------------------------
  read IGNORE
fi
if [ $BITS -eq 0 ]; then
  BITS="64"
else
  BITS=""
fi

# ---------------------------------------------------------------------
# Ensure IDE_HOME points to the directory where the IDE is installed.
# ---------------------------------------------------------------------
SCRIPT_LOCATION=$0
while [ -L "$SCRIPT_LOCATION" ]; do
  SCRIPT_LOCATION=`readlink -e "$SCRIPT_LOCATION"`
done

IDE_HOME=`dirname "$SCRIPT_LOCATION"`/..
IDE_BIN_HOME=`dirname "$SCRIPT_LOCATION"`

# ---------------------------------------------------------------------
# Collect JVM options and properties.
# ---------------------------------------------------------------------
if [ -n "$PYCHARM_PROPERTIES" ]; then
  IDE_PROPERTIES_PROPERTY="-Didea.properties.file=\"$PYCHARM_PROPERTIES\""
fi

MAIN_CLASS_NAME="$PYCHARM_MAIN_CLASS_NAME"
if [ -z "$MAIN_CLASS_NAME" ]; then
  MAIN_CLASS_NAME="com.intellij.idea.Main"
fi

VM_OPTIONS_FILE="$PYCHARM_VM_OPTIONS"
if [ -z "$VM_OPTIONS_FILE" ]; then
  VM_OPTIONS_FILE="$IDE_BIN_HOME/pycharm$BITS.vmoptions"
fi

if [ -r "$VM_OPTIONS_FILE" ]; then
  VM_OPTIONS=`cat "$VM_OPTIONS_FILE" | grep -ve "^#.*" | tr '\n' ' '`
  VM_OPTIONS="$VM_OPTIONS -Djb.vmOptionsFile=\"$VM_OPTIONS_FILE\""
fi

IS_EAP="false"
if [ "$IS_EAP" = "true" ]; then
  OS_NAME=`echo $OS_TYPE | tr '[:upper:]' '[:lower:]'`
  AGENT_LIB="yjpagent-$OS_NAME$BITS"
  if [ -r "$IDE_BIN_HOME/lib$AGENT_LIB.so" ]; then
    AGENT="-agentlib:$AGENT_LIB=disablej2ee,disablecounts,disablealloc,sessionname=PyCharm20"
  fi
fi

COMMON_JVM_ARGS="-Xbootclasspath/a:../lib/boot.jar -Didea.paths.selector=PyCharm20 $IDE_PROPERTIES_PROPERTY"
IDE_JVM_ARGS="-Didea.platform.prefix=Python -Didea.no.jre.check=true"
ALL_JVM_ARGS="$VM_OPTIONS $COMMON_JVM_ARGS $IDE_JVM_ARGS $AGENT $REQUIRED_JVM_ARGS"

CLASSPATH="../lib/bootstrap.jar"
CLASSPATH="$CLASSPATH:../lib/extensions.jar"
CLASSPATH="$CLASSPATH:../lib/util.jar"
CLASSPATH="$CLASSPATH:../lib/jdom.jar"
CLASSPATH="$CLASSPATH:../lib/log4j.jar"
CLASSPATH="$CLASSPATH:../lib/trove4j.jar"
CLASSPATH="$CLASSPATH:../lib/jna.jar"
if [ -n "$PYCHARM_CLASSPATH" ]; then
  CLASSPATH="$CLASSPATH:$PYCHARM_CLASSPATH"
fi
export CLASSPATH

export LD_LIBRARY_PATH="$IDE_BIN_HOME:$LD_LIBRARY_PATH"

# ---------------------------------------------------------------------
# Run the IDE.
# ---------------------------------------------------------------------
cd "$IDE_BIN_HOME"
while true ; do
  eval $JDK/bin/java $ALL_JVM_ARGS -Djb.restart.code=88 $MAIN_CLASS_NAME $*
  test $? -ne 88 && break
done
