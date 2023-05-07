#!/bin/sh
/opt/python-3.6/bin/python3 hw4_toPCFG.py "$1" "$2" 
/opt/python-3.6/bin/python3 hw4_parser.py -grammar "$2"  -test_file "$3" -out_file "$4"
/opt/python-3.6/bin/python3 hw4_improved_parser.py -grammar "$5"  -test_file "$3" -out_file "$6"
/dropbox/22-23/au571/hw4/tools/evalb -p /dropbox/22-23/au571/hw4/tools/COLLINS.prm /dropbox/22-23/au571/hw4/data/parses.gold "$4" > "$7"
/dropbox/22-23/au571/hw4/tools/evalb -p /dropbox/22-23/au571/hw4/tools/COLLINS.prm /dropbox/22-23/au571/hw4/data/parses.gold "$6" > "$8"