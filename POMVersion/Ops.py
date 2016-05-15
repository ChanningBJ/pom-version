import subprocess

import sys
from gitapi import gitapi
import untangle

__repo = None


def init():
    global __repo
    __repo = gitapi.Repo('.')


def git_path_changed(path, tag):
    global __repo
    tag_name = 'refs/tags/'+tag
    try:
        __repo.git_command('show-ref','--tags',tag_name)
    except Exception:
        print('Tag '+tag+' not found')
        return True # The tag is not defined

    result = __repo.git_command('diff-tree','--no-commit-id','--name-only','-r',tag_name+'..HEAD').split()
    print("Changed files:")
    for file in result:
        print file
    for file in result:
        if file.find(path) == 0:
            return True
    return False


def git_tag(tag_name):
    global __repo
    __repo.git_command('tag', tag_name)
    result = __repo.git_push(destination='origin',branch=tag_name)
    print result

def change_pom_version():
    global  __repo
    old_version = pom_get_version()
    print('Old Version: ' + str(old_version))
    version1 = old_version.split('.')
    version2 = version1[:-1]+[str(int(version1[-1])+1)]
    new_version = '.'.join(version2)
    print('New Version: '+str(new_version))

    print('Changing pom file')
    status = subprocess.call(['mvn','versions:set','-DnewVersion='+new_version])
    if status!=0:
        print('Failed change to new version')
        sys.exit(-1)
    status = subprocess.call(['mvn','versions:commit'])
    if status!=0:
        print('Failed change comit vew version')
        sys.exit(-1)
    print('Applied new version to pom file')
    __repo.git_command('commit','-a','-m','Change API version to '+new_version)
    __repo.git_push()
    return new_version

def pom_get_version():
    pom = untangle.parse('pom.xml')
    return pom.project.version.cdata

