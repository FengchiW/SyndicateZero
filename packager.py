from distutils.debug import DEBUG
import os
import sys
import argparse

__RAYLIB_COMPILER_ARGS = [
    '--std=c++23',
    '-g',
    '-Wall',
    '-D_DEFAULT_SOURCE',
    '-s',
    '-O1 release.res',
    '-I. -IC:/raylib/raylib/src',
    '-IC:/raylib/raylib/src/external',
    '-L. -LC:/raylib/raylib/src',
    '-LC:/raylib/raylib/src',
    '-lraylib',
    '-lopengl32',
    '-lgdi32',
    '-lwinmm',
    '-DPLATFORM_DESKTOP',
]

__DEBUG_FLAG = "-Wl,--subsystem,windows"

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Build and compile the project')
    parser.add_argument('-b', '--build', action='store_true', help='Build the project')
    parser.add_argument('-d', '--debug', action='store_true', help='Build the project in debug mode')
    parser.add_argument('-r', '--release', action='store_true', help='Build the project in release mode')
    parser.add_argument('-t', '--test', action='store_true', help='Build the project in test mode')
    parser.add_argument('-v', '--verbose', action='store_true', help='Build the project in verbose mode')
    args = parser.parse_args()

    # Build the project
    if args.build:
        # create a build directory if it doesn't exist
        if not os.path.exists('build'):
            os.makedirs('build')
        # build the project
        # look for any c++ files in src directory and compile them
        for file in os.listdir('src'):
            if file.endswith('.cpp'):
                if args.debug:
                    os.system('g++ -c ' + ' '.join(__RAYLIB_COMPILER_ARGS)
                     + ' ' + __DEBUG_FLAG + 
                     ' ' + 'src/' + file + 
                     ' -o build/debug/' + file.replace('.cpp', '.o'))
                else:
                    os.system('g++ -c ' + ' '.join(__RAYLIB_COMPILER_ARGS)
                     + ' ' + 'src/' + file + 
                     ' -o build/' + file.replace('.cpp', '.o'))
        # link the object files into a binary
        if args.debug:
            os.system('g++ -o build/debug.exe' + ' '.join(__RAYLIB_COMPILER_ARGS)
             + ' ' + __DEBUG_FLAG + 
             ' build/debug/*.o')
        else:
            os.system('g++ -o build/raylib.exe' + ' '.join(__RAYLIB_COMPILER_ARGS)
             + ' build/*.o')
            # remove the object files
            os.system('rm build/*.o')
        # copy the resources
        os.system('cp -r res build/')

        
if __name__ == '__main__':
    main()