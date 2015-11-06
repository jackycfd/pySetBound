#!/usr/bin/env python


"""Set OpenFOAM boundary condition."""

__author__ = "Zhihua Ma"

__version__ = "0.1"

import sys
import os
import re

typeNames=['patch','symmetryPlane','empty','wedge','cyclic','wall']

def hasPhysicalType(string):
    if 'physicalType' in string:
        return (True)
    else:
        return (False)

def hasType(string):
    if 'type' in string:
        return (True)
    else:
        return (False)


def hasBound(boundName,string):
    if boundName in string:
        return (True)
    else:
        return (False)

class Main:
    """Main program."""

    sourceFileName="./constant/polyMesh/boundary"
    targetFileName="./constant/polyMesh/boundary"

    def main(self):
        """Main program."""
        print "OpenFOAM boundary condition"

        numArgv=len(sys.argv)
        if numArgv != 3:
            print "wrong arguments"
            sys.exit()

        sourceBound=sys.argv[numArgv-1]
        targetType=sys.argv[numArgv-2]
        targetType=targetType.replace('-','')
        targetType=targetType.replace(' ','')

        print "sourceBound= %s" %(sourceBound)
        print "targetType = %s" %(targetType)

        if not(targetType in typeNames):
            print "the targetType is wrong"
            sys.exit()

        file=open(self.sourceFileName,"r")
        totalSourceFileLine=file.readlines()
        file.close()

        length=len(totalSourceFileLine)

        start=0
        end=0
        #look for sourceBound
        for i in range(0,length):
            line=totalSourceFileLine[i]
            if hasBound(sourceBound,line):
                start=i
             if hasBound('}',line) and start>0:
                end=i
                break

        print "start=%d end=%d" %(start,end)
        if start==0 or end==0:
            print "Warning!!!!"
            print "The bound <<%s>> is not found in the file"  %(sourceBound)
            sys.exit()

        for i in range(0,length):
            if hasPhysicalType(totalSourceFileLine[i]):
                totalSourceFileLine[i]='\n'

            if i>start and i<end and hasType(totalSourceFileLine[i]):
                print "***!!! To set the bound <<%s>> with <<%s>> condition" %(sourceBound,targetType)
                totalSourceFileLine[i]='\ttype\t\t'+targetType+';\n'

            
        #overwrite the file boundary under "./constant/polyMesh/boundary"
        file=open(self.targetFileName,"w")
        file.writelines(totalSourceFileLine)
        file.close()

if __name__ == '__main__':
    Main().main()
