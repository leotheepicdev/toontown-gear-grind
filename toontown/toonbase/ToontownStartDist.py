# This is included in the package by the builder script. It contains the
# (stripped) DC file and configuration.
from data import TTGGData

# Load all packaged config pages:
from panda3d.core import loadPrcFileData

for i, config in enumerate(TTGGData.CONFIG):
    loadPrcFileData('GameData Packaged Config Page #%d' % i, config)

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load them manually:

from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename, Multifile

import os

vfs = VirtualFileSystem.getGlobalPtr()
mfs = [3, 3.5, 4, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
abort = False

for mf in mfs:
    filename = 'resources/phase_{0}.mf'.format(mf)

    if not os.path.isfile(filename):
        print('Phase {0} not found!'.format(filename))
        abort = True
        break

    mf = Multifile()
    mf.openRead(filename)

    if not vfs.mount(mf, '/', 0):
        print('Unable to mount {0}!'.format(filename))
        abort = True
        break

vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')

for mount in mounts:
    mountFile, mountPoint = (mount.split(' ', 2) + [None, None, None])[:2]
    mountFile = Filename(mountFile)
    mountFile.makeAbsolute()
    mountPoint = Filename(mountPoint)
    vfs.mount(mountFile, mountPoint, 0)

# DC data is a little bit trickier... The stock ConnectionRepository likes to
# read DC from filenames only. DCFile does let us read in istreams, but there's
# really no way to pass the istream off through ConnectionRepository. We can stick
# the file on the vfs, but that's messy...

from panda3d.core import StringStream

dcStream = StringStream(TTGGData.DC)

from direct.distributed import ConnectionRepository
import types

class ConnectionRepository_override(ConnectionRepository.ConnectionRepository):

    def readDCFile(self, dcFileNames=None):
        """
        Reads in the dc files listed in dcFileNames, or if
        dcFileNames is None, reads in all of the dc files listed in
        the Config.prc file.
        """

        dcFile = self.getDcFile()
        dcFile.clear()
        self.dclassesByName = {}
        self.dclassesByNumber = {}
        self.hashVal = 0

        if isinstance(dcFileNames, str):
            # If we were given a single string, make it a list.
            dcFileNames = [dcFileNames]

        dcImports = {}
        readResult = dcFile.read(dcStream)
        if not readResult:
            self.notify.error("Could not read dc file.")

        # if not dcFile.allObjectsValid():
        #    names = []
        #    for i in range(dcFile.getNumTypedefs()):
        #        td = dcFile.getTypedef(i)
        #        if td.isBogusTypedef():
        #            names.append(td.getName())
        #    nameList = ', '.join(names)
        #    self.notify.error("Undefined types in DC file: " + nameList)

        self.hashVal = dcFile.getHash()

        # Now import all of the modules required by the DC file.
        for n in range(dcFile.getNumImportModules()):
            moduleName = dcFile.getImportModule(n)[:]

            # Maybe the module name is represented as "moduleName/AI".
            suffix = moduleName.split('/')
            moduleName = suffix[0]
            suffix = suffix[1:]
            if self.dcSuffix in suffix:
                moduleName += self.dcSuffix
            elif self.dcSuffix == 'UD' and 'AI' in suffix:  # HACK:
                moduleName += 'AI'

            importSymbols = []
            for i in range(dcFile.getNumImportSymbols(n)):
                symbolName = dcFile.getImportSymbol(n, i)

                # Maybe the symbol name is represented as "symbolName/AI".
                suffix = symbolName.split('/')
                symbolName = suffix[0]
                suffix = suffix[1:]
                if self.dcSuffix in suffix:
                    symbolName += self.dcSuffix
                elif self.dcSuffix == 'UD' and 'AI' in suffix:  # HACK:
                    symbolName += 'AI'

                importSymbols.append(symbolName)

            self.importModule(dcImports, moduleName, importSymbols)

        # Now get the class definition for the classes named in the DC
        # file.
        for i in range(dcFile.getNumClasses()):
            dclass = dcFile.getClass(i)
            number = dclass.getNumber()
            className = dclass.getName() + self.dcSuffix

            # Does the class have a definition defined in the newly
            # imported namespace?
            classDef = dcImports.get(className)
            if classDef is None and self.dcSuffix == 'UD':  # HACK:
                className = dclass.getName() + 'AI'
                classDef = dcImports.get(className)

            # Also try it without the dcSuffix.
            if classDef is None:
                className = dclass.getName()
                classDef = dcImports.get(className)
            if classDef is None:
                self.notify.debug("No class definition for %s." % className)
            else:
                if isinstance(classDef, types.ModuleType):
                    if not hasattr(classDef, className):
                        self.notify.warning(
                            "Module %s does not define class %s." %
                            (className, className))
                        continue
                    classDef = getattr(classDef, className)

                if not isinstance(
                        classDef,
                        type) and not isinstance(
                        classDef,
                        type):
                    self.notify.error(
                        "Symbol %s is not a class name." %
                        className)
                else:
                    dclass.setClassDef(classDef)

            self.dclassesByName[className] = dclass
            if number >= 0:
                self.dclassesByNumber[number] = dclass

        # Owner Views
        if self.hasOwnerView():
            ownerDcSuffix = self.dcSuffix + 'OV'
            # dict of class names (without 'OV') that have owner views
            ownerImportSymbols = {}

            # Now import all of the modules required by the DC file.
            for n in range(dcFile.getNumImportModules()):
                moduleName = dcFile.getImportModule(n)

                # Maybe the module name is represented as "moduleName/AI".
                suffix = moduleName.split('/')
                moduleName = suffix[0]
                suffix = suffix[1:]
                if ownerDcSuffix in suffix:
                    moduleName += ownerDcSuffix

                importSymbols = []
                for i in range(dcFile.getNumImportSymbols(n)):
                    symbolName = dcFile.getImportSymbol(n, i)

                    # Check for the OV suffix
                    suffix = symbolName.split('/')
                    symbolName = suffix[0]
                    suffix = suffix[1:]
                    if ownerDcSuffix in suffix:
                        symbolName += ownerDcSuffix
                    importSymbols.append(symbolName)
                    ownerImportSymbols[symbolName] = None

                self.importModule(dcImports, moduleName, importSymbols)

            # Now get the class definition for the owner classes named
            # in the DC file.
            for i in range(dcFile.getNumClasses()):
                dclass = dcFile.getClass(i)
                if (dclass.getName() + ownerDcSuffix) in ownerImportSymbols:
                    number = dclass.getNumber()
                    className = dclass.getName() + ownerDcSuffix

                    # Does the class have a definition defined in the newly
                    # imported namespace?
                    classDef = dcImports.get(className)
                    if classDef is None:
                        self.notify.error(
                            "No class definition for %s." %
                            className)
                    else:
                        if isinstance(classDef, types.ModuleType):
                            if not hasattr(classDef, className):
                                self.notify.error(
                                    "Module %s does not define class %s." %
                                    (className, className))
                            classDef = getattr(classDef, className)
                        dclass.setOwnerClassDef(classDef)
                        self.dclassesByName[className] = dclass

ConnectionRepository.ConnectionRepository = ConnectionRepository_override

# Okay, everything should be set now... Toontown, start!
import toontown.toonbase.ToontownStart