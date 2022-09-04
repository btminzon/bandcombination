
import xlsxwriter


def writeBandOnFile(workbook, bandsList, modulationList, nr_flag=False):
    # Add a worksheet to Excel file
    BandWorksheet = workbook.add_worksheet('Band Info')

    # Header
    BandCombinationHeader = ("LTE Band", "NR Band", "256QAM in DL", "64QAM in UL")

    # used formats on this worksheet
    cellHeaderFormat = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': 1, 'font_size': 14, })
    cellFormat = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': 0, 'font_size': 11, })

    row = 0
    col = 0

    for headerItem in BandCombinationHeader:
        BandWorksheet.write(row, col, headerItem, cellHeaderFormat)
        col += 1

    lterow = 1
    nrrow = 1
    col = 0
    for band, modulation in zip(bandsList, modulationList):
        if band.startswith('n'):
            BandWorksheet.write(nrrow, col+1, band, cellFormat)
            nrrow += 1
        else:
            BandWorksheet.write(lterow, col, band, cellFormat)
            BandWorksheet.write(lterow, col+2, modulation['dl-256QAM-r12'], cellFormat)
            BandWorksheet.write(lterow, col+3, modulation['ul-64QAM-r12'], cellFormat)
            lterow += 1

    # set LTE Band column size to 10
    BandWorksheet.set_column(0, 0, 10)

    # set NR Band column size to 10
    BandWorksheet.set_column(1, 1, 10, None, {'hidden': not nr_flag})

    # set 256QAM column size to 17
    BandWorksheet.set_column(2, 2, 17, None, {'hidden': nr_flag})

    # set 64QAM column size to 16
    BandWorksheet.set_column(3, 3, 16, None, {'hidden': nr_flag})


def writeBandCombinationOnFile(workbook, bandCombinationList, layersList, bcsList, nr_flag=False):

    # No Carrier Aggregation Support
    if bandCombinationList == ["None"]:
        return

    # Add a worksheet to Excel file
    BandCombinationWorksheet = workbook.add_worksheet('Band Combination Info')

    # Header
    BandCombinationHeader = ("Item", "Band Combination", "BW Class", "MIMO", "Layers", "Bandwidth Combination Set*")

    # used formats on this worksheet
    cellHeaderFormat = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': 1, 'font_size': 14, })
    cellFormat = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': 0, 'font_size': 11, })
    itemCellFormat = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': 1, 'font_size': 11, })
    noteFormat = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'border': 1, 'bold': 1, 'font_size': 11, })

    row = 0
    col = 0

    for headerItem in BandCombinationHeader:
        BandCombinationWorksheet.write(row, col, headerItem, cellHeaderFormat)
        col += 1

    row = 1
    col = 0
    ItemIndex = 0
    notMerged = True
    if nr_flag:
        for items in bandCombinationList:
            BandCombinationWorksheet.write(row, col, ItemIndex, itemCellFormat)
            bandCombination = ""
            for bandCombinationObject in items:
                bandCombination = ''.join((bandCombination, bandCombinationObject['Band']))
                bandCombination = ''.join((bandCombination, bandCombinationObject['BwClass'].upper()))
                bandCombination = bandCombination + '_'
            bandCombination = bandCombination[:-1]  # remove the last '_'
            BandCombinationWorksheet.write(row, col + 1, bandCombination, cellFormat)
            col = 0
            row += 1
            ItemIndex += 1
    else:
        for items in bandCombinationList:
            for bandCombinationObject in items:
                if len(items) > 1 and notMerged:
                    BandCombinationWorksheet.merge_range(row, col, row + len(items) - 1, col,
                                                         bandCombinationObject['Item'], itemCellFormat)
                    BandCombinationWorksheet.merge_range(row, col + 4, row + len(items) - 1, col + 4,
                                                         layersList[ItemIndex], cellFormat)
                    BandCombinationWorksheet.merge_range(row, col + 5, row + len(items) - 1, col + 5,
                                                  "ALL" if bcsList[ItemIndex] == "" else bcsList[ItemIndex], cellFormat)
                    notMerged = False
                elif len(items) == 1:
                    BandCombinationWorksheet.write(row, col, bandCombinationObject['Item'], itemCellFormat)
                    BandCombinationWorksheet.write(row, col + 4, layersList[ItemIndex], cellFormat)
                    BandCombinationWorksheet.write(row, col + 5,
                                                "ALL" if bcsList[ItemIndex] == '' else bcsList[ItemIndex], cellFormat)
                BandCombinationWorksheet.write(row, col + 1, bandCombinationObject['Band'], cellFormat)
                BandCombinationWorksheet.write(row, col + 2, bandCombinationObject['BwClass'].upper(), cellFormat)
                BandCombinationWorksheet.write(row, col + 3, "2x2" if bandCombinationObject[
                                                    'SupportedMIMOLayers'] == 'twoLayers' else "4x4", cellFormat)
                col = 0
                row += 1
            notMerged = True
            ItemIndex += 1

    # set Band column size to 21
    BandCombinationWorksheet.set_column(1, 1, 21)

    # set BW Class column size to 11
    BandCombinationWorksheet.set_column(2, 2, 11, None, {'hidden': nr_flag})

    # FIXME hidding columns not handled yet
    # set MIMO column size to 11
    BandCombinationWorksheet.set_column(3, 3, 11, None, {'hidden': nr_flag})

    # set Layers column size to 11
    BandCombinationWorksheet.set_column(4, 4, 11, None, {'hidden': nr_flag})

    # set BCS column size to 28
    BandCombinationWorksheet.set_column(5, 5, 44, None, {'hidden': nr_flag})

    # FIXME Hide note if in NR. Unhide when parse correctly
    if nr_flag is False:
        # Write a note about where to find BCS definition, in 3gpp
        BandCombinationWorksheet.merge_range(row, 0, row, col + 5,
                        "* For BCS information, please check 36.301-Rel15 tables 5.6A.1-1 and  5.6A.1-2", noteFormat)


def write2Excel(bandsList, bandCombinationList, layersList, bcsList, modulationList, file, nr_flag=False):
    # filename
    workbook = xlsxwriter.Workbook(file)

    # Write supported bands and related items
    writeBandOnFile(workbook, bandsList, modulationList, nr_flag)

    # Write supported band combination items and related features
    writeBandCombinationOnFile(workbook, bandCombinationList, layersList, bcsList, nr_flag)

    print("Created file {}".format(file))

    # close file
    workbook.close()
