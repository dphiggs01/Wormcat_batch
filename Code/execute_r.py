from subprocess import Popen, PIPE
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class ExecuteR(object):
    worm_cat_function = ('./worm_cat.R',
                               '--file', 0,
                               '--title', 1,
                               '--out_dir', 2,
                               '--rm_dir', 3,
                               '--annotation_file',4,
                               '--input_type', 5
                               )
    wormcat_library_path = ('./is_wormcat_installed.R','--no-save',0, '--quiet',1)

    def wormcat_library_path_fun(self):
        ret_val = self.run(self.wormcat_library_path,"")
        return ret_val

    def worm_cat_fun(self, file_name, out_dir, title="rgs", annotation_file="straight", input_type="Sequence ID"):
        ret_val = self.run(self.worm_cat_function, file_name, title, out_dir, "False", annotation_file, input_type)
        return ret_val



    def run(self, arg_list, *args):
        try:
            processed_args = self.process_args(arg_list, *args)
            process = Popen(processed_args, stdout=PIPE)
            out, err = process.communicate()
            out = str(out, 'utf-8')
            if not out:
                out = None
            #sys.stderr.write("run: out={} err={}\n".format(out,err))
            return out
        except Exception as e:
            sys.stderr.write("ERROR: command line error %s\n" % args)
            sys.stderr.write("ERROR: %s\n" % e)
            sys.exit(-1)

    def process_args(self, arg_tuple, *args):
        # process the arg
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
