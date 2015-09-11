#!/bin/bash

#  Created by: TheZero
#  Modified & Distributed by: Lorenzo 'EclipseSpark' Faletra <eclipse@frozenbox.org>
#
#
#  v. 1.8.1
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
 

 
export BLUE='\033[1;94m'
export GREEN='\033[1;92m'
export RED='\033[1;91m'
export RESETCOLOR='\033[1;00m'
 
build(){
	cp "$ARCHIVE_FULLPATH" build-$ARCHIVE_FULLPATH
	cd build-$ARCHIVE_FULLPATH
    find . -type f -exec md5sum {} + > DEBIAN/md5sums
    cd ..
    chown root:root -R build-$ARCHIVE_FULLPATH | true
    if [ "$VERBOSE" == "" ]; then
		cmd=`dpkg-deb -b "$ARCHIVE_FULLPATH"`
	else
		dpkg-deb -b "$ARCHIVE_FULLPATH"
    fi
    if [ "$KEEP" == "n" ]; then
		rm -f$VERBOSE -R "$ARCHIVE_FULLPATH"
    fi
    rm -r build-$ARCHIVE_FULLPATH
}


extract(){
	if [[ -e "$NEWDIRNAME" ]]; then
		if [ "$KEEP" == "n" ]; then
			rm -f$VERBOSE -R "$NEWDIRNAME"
			mkdir "$NEWDIRNAME"
		fi
	else
	    mkdir "$NEWDIRNAME"
	fi
    cp -f$VERBOSE -R "$ARCHIVE_FULLPATH" "$NEWDIRNAME"
    cd "$NEWDIRNAME"
    ar ${VERBOSE}x "$FILENAME"
	rm -f$VERBOSE -R "$FILENAME"
    for FILE in *.tar.gz; do [[ -e $FILE ]] && tar x${VERBOSE}pf $FILE; done
    for FILE in *.tar.xz; do [[ -e $FILE ]] && tar x${VERBOSE}pf $FILE; done
    for FILE in *.tar.lzma; do [[ -e $FILE ]] && tar x${VERBOSE}pf $FILE; done
    [[ -e "control.tar.gz" ]] && rm -f$VERBOSE -R "control.tar.gz"
    [[ -e "control.tar.xz" ]] && rm -f$VERBOSE -R "control.tar.xz"
    [[ -e "control.tar.bz2" ]] && rm -f$VERBOSE -R "control.tar.bz2"
    [[ -e "control.tar.lzma" ]] && rm -f$VERBOSE -R "control.tar.lzma"
    [[ -e "data.tar.gz" ]] && rm -f$VERBOSE -R "data.tar.gz"
    [[ -e "data.tar.bz2" ]] && rm -f$VERBOSE -R "data.tar.bz2"
    [[ -e "data.tar.xz" ]] && rm -f$VERBOSE -R "data.tar.xz"
    [[ -e "data.tar.lzma" ]] && rm -f$VERBOSE -R "data.tar.lzma"
    [[ -e "debian-binary" ]] && rm -f$VERBOSE -R "debian-binary"

    if [[ -e "DEBIAN" ]]; then
		if [ "$KEEP" == "n" ]; then
			rm -f$VERBOSE -R "DEBIAN"
			mkdir "DEBIAN"
		fi
	else
	    mkdir "DEBIAN"
	fi
    [[ -e "changelog" ]] && mv -f$VERBOSE "changelog" "DEBIAN"
    [[ -e "config" ]] && mv -f$VERBOSE "config" "DEBIAN"
    [[ -e "conffiles" ]] && mv -f$VERBOSE "conffiles" "DEBIAN"
    [[ -e "control" ]] && mv -f$VERBOSE "control" "DEBIAN"
    [[ -e "copyright" ]] && mv -f$VERBOSE "copyright" "DEBIAN"
    [[ -e "postinst" ]] && mv -f$VERBOSE "postinst" "DEBIAN"
    [[ -e "preinst" ]] && mv -f$VERBOSE "preinst" "DEBIAN"
    [[ -e "prerm" ]] && mv -f$VERBOSE "prerm" "DEBIAN"
    [[ -e "postrm" ]] && mv -f$VERBOSE "postrm" "DEBIAN"
    [[ -e "rules" ]] && mv -f$VERBOSE "rules" "DEBIAN"
    [[ -e "shlibs" ]] && mv -f$VERBOSE "shlibs" "DEBIAN"
    [[ -e "templates" ]] && mv -f$VERBOSE "templates" "DEBIAN"
    [[ -e "triggers" ]] && mv -f$VERBOSE "triggers" "DEBIAN"
    [[ -e ".svn" ]] && mv -f$VERBOSE ".svn" "DEBIAN"

    [[ -e "md5sums" ]] && rm -f$VERBOSE -R "md5sums"
}


# Program Main #
KEEP="y"
VERBOSE=""
ACTION="n"

while getopts ":b:x:kv" opt; do
  case $opt in
    b)
      ACTION="b"
      ARCHIVE_FULLPATH="$2"
	  NEWDIRNAME=${ARCHIVE_FULLPATH%.*}
      ;;
    x)
      ACTION="x"
      ARCHIVE_FULLPATH="$2"
	  NEWDIRNAME=${ARCHIVE_FULLPATH%.*}
	  FILENAME=${ARCHIVE_FULLPATH##*/}
      ;;
    k)
      KEEP="y"
      ;;
    v)
      VERBOSE="v"
      ;;
    \?)
      echo "$RED Invalid option:$GREEN -$OPTARG$RESETCOLOR" >&2
      exit 1
      ;;
    :)
      echo "$RED Option$GREEN -$OPTARG$RED requires an argument.$RESETCOLOR" >&2
      exit 1
      ;;
  esac
done

if [ $ACTION == "b" ]; then
	build
elif [ $ACTION == "x" ]; then
	extract
elif [ $ACTION == "n" ]; then
	echo -e "$BLUE Usage: \n\t$GREEN -b [file_path]\t$RED -> Build DEB\n\t$GREEN -x [dir_path]\t$RED -> Extract DEB \n\t$GREEN -k\t\t$REN -> Keep File\n\t$GREEN -v\t\t$RED -> Verbose$RESETCOLOR"
	exit 1
fi

exit 0
