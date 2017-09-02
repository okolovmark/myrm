# myrm
clone rm with buns

Usage: myrm [OPTIONS] COMMAND [ARGS]...

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
  --help                       Show this message and exit.

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
