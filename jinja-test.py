#!/usr/bin/env python

import getopt
import jinja2
import os
import sys
import time
import yaml

import filters.salt

# load pillar
def load_pillar(pillar_file):
    with open(pillar_file, 'r') as stream:
        try:
            pillar = yaml.load(stream)
        except yaml.YAMLError as e:
            print(e)
    return pillar

# Common Timestamp Helper
def timestamp():
    return time.strftime('%d/%b/%Y:%H:%M:%S %z', time.gmtime())


class JTest:

    def __init__(self,pillar,template_file):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.env = jinja2.Environment(
                loader = jinja2.FileSystemLoader(self.dir_path)
                )
        self.template = self.env.get_template(template_file)
        print "Pillar data:\n\t %s" % pillar
        print "Template:"
        print self.template.render(pillar)


def usage():
    print "Usage: %s -p <pillar_file> -t <template_file>\n" % (__file__)
    print "Options:"
    print "\t-h, --help\t\tPrints this help"
    print "\t-d, --demo\t\tRuns with demo files"
    print "\t-p, --pillar\t\tSpecify the pillar file to use"
    print "\t-t, --template\t\tSpecify the template to use"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdp:t:", ["help", "demo", "pillar=", "template="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print "\nERROR: %s" % str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    pillar_file = 'pillars/demo.yaml.demo'
    template_file = 'templates/demo.j2.demo'
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--demo"):
            JTest(pillar, template)
        elif o in ("-p", "--pillar"):
            pillar_file = a
        elif o in ("-t", "--template"):
            template_file = a
        else:
            assert False, "unhandled option"
    pillar = load_pillar(pillar_file)
    JTest(pillar,template_file)


# Main
if __name__ == "__main__":
    main()
