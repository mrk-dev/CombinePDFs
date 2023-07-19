import argparse

import combine_helper as ch
from combine_gui import Application, create_window


def setup_args():
    parser = argparse.ArgumentParser("combine.py")
    parser.add_argument("pdf_folder", type=str, 
        help="folder containing pdf files")
    parser.add_argument("outfile_name", type=str, 
        help="output pdf file name")
    parser.add_argument("-w", "--window", action="store_true", dest="window", 
        help="start with GUI")
    parser.add_argument("-m", "--monitor", type=int, metavar="N", dest="monitor", default=-1, 
        help="monitor source pdf folder every N seconds and automatically generate combined file.")
    
    return parser


def run_window_mode(source_folder, output_file, monitor_delay):
    source_folder = None if source_folder == "#" else source_folder
    output_file = None if output_file == "#" else output_file
    monitor_delay = -1 if monitor_delay < 0 else monitor_delay

    window = create_window()
    app = Application(window, source_folder, output_file, monitor_delay)
    app.mainloop()
    window.destroy()


# ====================================MAIN====================================
#
if __name__ == '__main__':
    argsparser = setup_args()
    args = argsparser.parse_args()

    try:
        if args.window:
            # launch window gui
            print("GUI")
            run_window_mode(args.pdf_folder, args.outfile_name, args.monitor)
        else:
            if args.monitor:
                ch.monitorpdfs(args.pdf_folder, args.outfile_name, args.monitor)
            else:
                ch.combinepdfs(args.pdf_folder, args.outfile_name)
    except Exception as e:
        print("***ERROR*** {0}".format(e))
