#!/bin/bash
# Run the pacman game with python ai player

DIR_PATH=`pwd`
JAR_PATH="$DIR_PATH/pacman-python.jar"
JYTHON_LIB="$DIR_PATH/jython.jar/Lib"
SRC_PATH="$DIR_PATH/player"

# Run
java -jar $JAR_PATH $JYTHON_LIB $SRC_PATH $@