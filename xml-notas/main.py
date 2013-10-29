#!/usr/bin/python

""" Program for generating a csv file with information about "Nota Fiscais".

By Flavio Diez
27/10/2013
"""

import os
import sys
import xml.etree.ElementTree as ET


def listXML(path):
    """
    Create a list with all the XML files to be analyzed

    :return xmls: list with files
    """
    xmls = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f[-3:].lower() == "xml":
                xmls.append("{0}/{1}".format(root, f))

    return xmls


def parseXML(xml):
    """
    The XMl is going to be parsed for the desired tags and are going to be organized into a csv format

    :return csv: String as a CSV file format
    """
    _PRE_TAG = '{http://www.portalfiscal.inf.br/nfe}'
    tags = ["nNF", "dEmi", "dest", "det"]
    destTags = ["CNPJ"]
    detTags = ["cProd", "xProd", "NCM", "CFOP", "qCom", "vUnCom", "imposto"]
    impostoTags = ["ICMS", "IPI"]
    icmsTags = ["CST", "vBC", "pICMS"]
    ipiTags = ["pIPI"]

    csv = []

    # Variable initialization
    nNF = dEmi = destCNPJ = nItem = cProd = xProd = ncm = cst = "#"
    cfop = qcom = vuncom = aliqICMS = bTribICMS = aliqIPI = "#"

    # Work on tree root and walk to find relevant nodes
    tree = ET.parse(xml)
    root = tree.getroot()

    for node in root.iter():
        try:
            if node.tag == _PRE_TAG+tags[0]:
                tagOfTurn = tags.pop(0)

                if tagOfTurn == "nNF":
                    nNF = node.text

                elif tagOfTurn == "dEmi":
                    dEmi = node.text

                elif tagOfTurn == "dest":

                    for subNode in node.iter():

                        if subNode.tag == _PRE_TAG+destTags[0]:
                            subTagOfTurn = destTags.pop(0)

                            if subTagOfTurn == "CNPJ":
                                destCNPJ = subNode.text

                        if len(destTags) == 0:
                            #Found everything
                            break

                elif tagOfTurn == "det":
                    nItem = node.attrib["nItem"]

                    for subNode in node.iter():
                        if subNode.tag == _PRE_TAG+detTags[0]:
                            subTagOfTurn = detTags.pop(0)

                            if subTagOfTurn == "cProd":
                                cProd = subNode.text
                            elif subTagOfTurn == "xProd":
                                xProd = subNode.text
                            elif subTagOfTurn == "NCM":
                                ncm = subNode.text
                            elif subTagOfTurn == "CFOP":
                                cfop = subNode.text
                            elif subTagOfTurn == "qCom":
                                qcom = subNode.text
                            elif subTagOfTurn == "vUnCom":
                                vuncom = subNode.text
                            elif subTagOfTurn == "imposto":
                                for item in subNode.iter():
                                    if item.tag == _PRE_TAG+impostoTags[0]:
                                        imposto = impostoTags.pop(0)

                                        if imposto == "ICMS":

                                            for impItem in item.iter():
                                                if impItem.tag == _PRE_TAG+icmsTags[0]:
                                                    tagOT = icmsTags.pop(0)

                                                    if tagOT == "CST":
                                                        cst = impItem.text
                                                    elif tagOT == "pICMS":
                                                        aliqICMS = impItem.text
                                                    elif tagOT == "vBC":
                                                        bTribICMS = impItem.text

                                                    if len(icmsTags) == 0:
                                                        # Found everything on this level. Reset and break
                                                        icmsTags = ["CST", "vBC", "pICMS"]
                                                        break

                                        elif imposto == "IPI":
                                            for impItem in item.iter():
                                                if impItem.tag == _PRE_TAG+ipiTags[0]:
                                                    tagOT = ipiTags.pop(0)

                                                    if tagOT == "pIPI":
                                                        aliqIPI = impItem.text

                                                    if len(ipiTags) == 0:
                                                        # Found everything on this level. Reset and break
                                                        ipiTags = ["pIPI"]
                                                        break

                                        if len(impostoTags) == 0:
                                            #Found everything for this item so reset it and break
                                            impostoTags = ["ICMS", "IPI"]
                                            break

                        if len(detTags) == 0:
                            #Found everything for this item so reset it and break
                            detTags = ["cProd", "xProd", "NCM", "CFOP", "qCom", "vUnCom", "imposto"]
                            break

                    # After an Item is completed a row from the csv file should be created
                    row = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13}\n".format(nNF, dEmi, destCNPJ,
                                                                                                 nItem, cProd, xProd,
                                                                                                 ncm, cfop, qcom,
                                                                                                 vuncom, cst, aliqICMS,
                                                                                                 bTribICMS, aliqIPI)
                    #And vars should be reseted
                    nItem = cProd = xProd = ncm = cst = "#"
                    cfop = qcom = vuncom = aliqICMS = bTribICMS = aliqIPI = "#"

                    csv.append(row)
                    tags.append("det")
                if len(tags) == 0:
                    #Found everything
                    break
        except IndexError:
            break

    return csv


def init_with_gui():
    """
    Start the program with the graphical user interface.
    """
    printInfo("Will be implemented...\nSorry for the inconvenience...\n\n")


def main(searchPath, outputFile="output"):
    """
    Start program without the graphical user interface (GUI).
    It has the same functionality but not ease of use of the GUI.

    :param searchPath: The path to the folders where to look for the XML files
    :type searchPath: String
    """
    lis = listXML(searchPath)

    printInfo("-------------------------\nFound {0} XML files\n".format(len(lis)))

    with open(outputFile+".csv", "w") as outFile:
        # write headers from CSV
        outFile.write("Nro NF, Data Emissao, CNPJ Dest, item da NF," +
                      "codigo, descricao, NCM, CFOP, Qtda, Valor Unitario, CST," +
                      "Aliquota ICMS, base Trib ICMS, Aliquota IPI\n")

        # Write each row
        count = 1
        for xmlFile in lis:
            printInfo("Processing file {0:3} of {1:3}\r".format(count, len(lis)))
            for line in parseXML(xmlFile):
                outFile.write(line)
            count += 1
        printInfo("\n\n")


def printInfo(txt):
    sys.stdout.write(txt)
    sys.stdout.flush()


def helpInfo():
    print """
    usage without GUI:
        python main.py PATH_TO_FILE [options]

        options:
            -o  : output file name. (extension is csv)

    usage with GUI:
        python main.py -gui
    """
    pass


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        helpInfo()
    elif sys.argv[1].lower() == "-gui":
        init_with_gui()
    elif "-h" in sys.argv or "--help" in sys.argv:
        helpInfo()
    elif not os.path.exists(sys.argv[1]):
        print "NOT A VALID PATH!"
    else:
        if "-o" in sys.argv:
            outName = sys.argv.index("-o") + 1
            main(sys.argv[1], sys.argv[outName])
        else:
            main(sys.argv[1])
