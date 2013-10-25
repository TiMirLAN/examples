# coding=utf-8
from subprocess import call
from os.path import join


def build_requirements_txt_in(in_directory):
    try:
        with open(join(in_directory, 'requirements.txt'), 'w+') as requirements:
            call(['pip', 'freeze'], stdout=requirements)
    except Exception, e:
        print 'Requirements not stored'
        try:
            with open(join(in_directory, 'requirements.exception.log'), 'w+') as log:
                log.write(e)
        except Exception:
            print 'Can not create log file'
