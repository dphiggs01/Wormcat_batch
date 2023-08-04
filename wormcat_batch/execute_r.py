"""
Module to delegate calls to R program execution
"""
from subprocess import Popen, PIPE
import sys
import os
import platform
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class ExecuteR(object):
    """
    Class to mange R exection
    """
    wormcat_r = f'{os.path.dirname(__file__)}{os.path.sep}worm_cat.R'

    worm_cat_function = [wormcat_r,
                               '--file', 0,
                               '--title', 1,
                               '--out_dir', 2,
                               '--rm_dir', 3,
                               '--annotation_file',4,
                               '--input_type', 5,
                               '--zip_files', 6
                               ]

    is_wormcat_installed = f'{os.path.dirname(__file__)}{os.path.sep}is_wormcat_installed.R'
    wormcat_library_path = [is_wormcat_installed, '--no-save', 0, '--quiet', 1]

    if platform.system() == 'Windows':
        wormcat_library_path.insert(0,'rscript.exe')
        worm_cat_function.insert(0,'rscript.exe')


    def wormcat_library_path_fun(self):
        """
        Utility function to get the R library path to the Wormcat function
        """
        ret_val = self.run(self.wormcat_library_path,"")
        return ret_val

    def worm_cat_fun(self, file_name, out_dir, title, annotation_file, input_type):
        """
        Utility function to setup the call to Wormcat function
        """
        print(f"Calling Wormcat with {os.path.basename(file_name)[:-4]} data")
        ret_val = self.run(self.worm_cat_function, file_name, title, out_dir, "False", annotation_file, input_type, "False")
        return ret_val

    def run(self, arg_list, *args):
        """
        Execute the R script
        """
        try:
            processed_args = self.process_args(arg_list, *args)
            process = Popen(processed_args, stdout=PIPE)
            out, err = process.communicate()
            out = str(out, 'utf-8')
            if not out:
                out = None
            #sys.stderr.write("run: out={} err={}\n".format(out,err))
            return out
        except Exception as err:
            sys.stderr.write(f"ERROR: command line error {args}\n")
            sys.stderr.write(f"ERROR: %{err}\n")
            sys.exit(-1)

    def process_args(self, arg_tuple, *args):
        """
        Utility function to build the arg list
        """
        arg_list = list(arg_tuple)
        for index in range(0, len(arg_list)):
            if type(arg_list[index]) == int:
                # substitue for args passed in
                if arg_list[index] < len(args):
                    arg_list[index] = args[arg_list[index]]
                # if we have more substitutions than args passed delete the extras
                else:
                    del arg_list[index - 1:]
                    break
        return arg_list
