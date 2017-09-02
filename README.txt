About:
Program allows you to delete and restore folders and files


Project structure:
myrm
  additional_functions.py
  config.py
  converter_to_JSON.py
  edit_config.py
  main_logic.py
  myrm.py
  README.txt
  setup.py

Install:
Write "pip -e ." in the terminal

Config formats:
JSON:
{
    "call_auto_cleaning_if_memory_error": false,
    "dry": false,
    "last_cleaning_date": {
        "day": 3,
        "hour": 0,
        "microsecond": 139774,
        "minute": 57,
        "month": 9,
        "second": 8,
        "year": 2017
    },
    "level_log": 10,
    "max_size_for_start_cleaning": 2000000000,
    "min_day_for_start_cleaning": 14,
    "path_to_log": ".log_myrm_itislogfilemyrm_",
    "path_to_trash": ".trash",
    "policy": 0,
    "resolve_conflict": false,
    "show_bar_status": false,
    "silent": false,
    "with_confirmation": false
}

txt:
call_auto_cleaning_if_memory_error=false
dry=false
last_cleaning_date=(
day=2
hour=2
microsecond=489405
minute=23
month=9
second=21
year=2017
)
level_log=10
max_size_for_start_cleaning=2000000000
min_day_for_start_cleaning=14
path_to_log=".log_myrm_itislogfilemyrm_"
path_to_trash=".trash"
policy=false
show_bar_status=false
silent=false
with_confirmation=false
resolve_conflict=true


More detailed information about each configuration parameter
can be read in the terminal using the following command:
"myrm settings --help"

Usage:
myrm [OPTIONS] COMMAND [ARGS]...

  Here you can specify one-time settings, if you want and call the program
  functions.
  Example: "myrm -o -d clear_trash".
  Use --help for COMMAND for read help.

Options:
  -f, --file_of_settings TEXT  One-time settings from file, if it is specified
                               then one_time_settings is ignored
  -o, --one_time_settings      One-time settings, if false, then the other
                               lower options is ignored.
  -d, --dry                    Imitation of program.
  -s, --silent                 Program operation without reports.
  -w, --with_confirmation      All actions require confirmation.
  -p, --policy                 Select the trash cleaning policy: True=size,
                               False=time.
  -a, --auto_cleaning          Call function auto_clear_trash if memory is
                               full.
  -b, --show_bar_status        Show bar status.
  -t, --time INTEGER           Change the time at which the trash will be
                               cleaned(recommended: --time=10).
  -z, --size INTEGER           Change the size(byte) at which the trash will
                               be cleaned(recommended: --size=2000000000).
  -l, --level_log INTEGER      Change the level of the logging or omit the
                               parameter to disable logging.
  -r, --resolve_conflict       Resolve a conflict of files.


Commands:
  clear_trash        Clear the contents of the trash.
  delete_by_pattern  delete files by pattern in the trash.
  delete_files       delete files in the trash.
  load_txt_config    Loads the txt configuration file.
  new_log_path       Specify the path to the log.
  new_trash_path     Specify the path to the trash.
  restore_files      restore files from the trash.
  settings           Editing program settings.
  show_trash         Show the contents of the basket in quantity 'number'.
