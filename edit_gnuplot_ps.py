# To do:
# - Pent is not working.


import sys
import os
from shutil import move


def change_gnuplot_point_styles(fn):
    if not os.path.exists(fn):
        raise RuntimeError("file \"{}\" does not exist".format(fn))
    fntmp = fn
    while True:
        fntmp = fntmp+".tmp"
        if not os.path.exists(fntmp):
            break


    with open(fntmp, "w") as fout:
        with open(fn, "r") as fin:
            l = fin.readline()
            while l:

                # Change definitions.
                #if l[0:6] == "/Pent ":
                #    l2 = fin.readline()
                #    l3 = fin.readline()
                #    if l != "/Pent {stroke [] 0 setdash 2 copy gsave\n" or \
                #            l2 != "  translate 0 hpt M 4 {72 rotate 0 hpt L} repeat\n" or \
                #            l3 != "  closepath stroke grestore Pnt} def\n":
                #        raise RuntimeError("Some problem with Pent.")
                #    fout.write("/Pent {stroke [] 0 setdash 2 copy gsave\n  translate 0 hpt M 4 {72 rotate 0 hpt L} repeat\n  closepath fill\n  grestore 0 0 0 setrgbcolor closepath stroke} def\n")

                if l[0:5] == "/Dia ":
                    l2 = fin.readline()
                    l3 = fin.readline()
                    l4 = fin.readline()
                    if l != "/Dia {stroke [] 0 setdash 2 copy vpt add M\n" or \
                            l2 != "  hpt neg vpt neg V hpt vpt neg V\n" or \
                            l3 != "  hpt vpt V hpt neg vpt V closepath stroke\n" or \
                            l4 != "  Pnt} def\n":
                        raise RuntimeError("Some problem with Dia.")
                    fout.write("/Dia {stroke [] 0 setdash vpt add M\n  hpt neg vpt neg V hpt vpt neg V\n  hpt vpt V hpt neg vpt V closepath gsave fill grestore 0 0 0 setrgbcolor closepath stroke\n  } def\n")

                elif l[0:6] == "/TriU ":
                    l2 = fin.readline()
                    l3 = fin.readline()
                    l4 = fin.readline()
                    l5 = fin.readline()
                    if l != "/TriU {stroke [] 0 setdash 2 copy vpt 1.12 mul add M\n" or \
                            l2 != "  hpt neg vpt -1.62 mul V\n" or \
                            l3 != "  hpt 2 mul 0 V\n" or \
                            l4 != "  hpt neg vpt 1.62 mul V closepath stroke\n" or \
                            l5 != "  Pnt} def\n":
                        raise RuntimeError("Some problem with TriU.")
                    fout.write("/TriU {stroke [] 0 setdash vpt 1.12 mul add M\n  hpt neg vpt -1.62 mul V\n  hpt 2 mul 0 V\n  hpt neg vpt 1.62 mul V closepath gsave fill grestore 0 0 0 setrgbcolor closepath stroke\n  } def\n")

                elif l[0:6] == "/TriD ":
                    l2 = fin.readline()
                    l3 = fin.readline()
                    l4 = fin.readline()
                    l5 = fin.readline()
                    if l != "/TriD {stroke [] 0 setdash 2 copy vpt 1.12 mul sub M\n" or \
                            l2 != "  hpt neg vpt 1.62 mul V\n" or \
                            l3 != "  hpt 2 mul 0 V\n" or \
                            l4 != "  hpt neg vpt -1.62 mul V closepath stroke\n" or \
                            l5 != "  Pnt} def\n":
                        raise RuntimeError("Some problem with TriD.")
                    fout.write("/TriD {stroke [] 0 setdash vpt 1.12 mul sub M\n  hpt neg vpt 1.62 mul V\n  hpt 2 mul 0 V\n  hpt neg vpt -1.62 mul V closepath gsave fill grestore 0 0 0 setrgbcolor closepath stroke\n  } def\n")

                elif l[0:8] == "/Circle ":
                    l2 = fin.readline()
                    if l != "/Circle {stroke [] 0 setdash 2 copy\n" or \
                            l2 != "  hpt 0 360 arc stroke Pnt} def\n":
                        raise RuntimeError("Some problem with Circle.")
                    fout.write("/Circle {stroke [] 0 setdash \n  hpt 0 360 arc gsave fill grestore 0 0 0 setrgbcolor closepath stroke} def\n")

                elif l[0:5] == "/Box ":
                    l2 = fin.readline()
                    l3 = fin.readline()
                    l4 = fin.readline()
                    if l != "/Box {stroke [] 0 setdash 2 copy exch hpt sub exch vpt add M\n" or \
                            l2 != "  0 vpt2 neg V hpt2 0 V 0 vpt2 V\n" or \
                            l3 != "  hpt2 neg 0 V closepath stroke\n" or \
                            l4 != "  Pnt} def\n":
                        raise RuntimeError("Some problem with Box.")
                    fout.write("/Box {stroke [] 0 setdash exch hpt sub exch vpt add M\n  0 vpt2 neg V hpt2 0 V 0 vpt2 V\n  hpt2 neg 0 V closepath gsave fill grestore 0 0 0 setrgbcolor closepath stroke\n  } def\n")

                # Change all plots with Circle, Box, Pent, TriU, TriD, Dia.
                elif l[0:14] == "% Begin plot #":
                    fout.write(l)
                    l = fin.readline()
                    while l:
                        ws = l.split()
                        if ws[len(ws)-1] == "Circle" or ws[len(ws)-1] == "Box" \
                                or ws[len(ws)-1] == "Pent" \
                                or ws[len(ws)-1] == "TriU" \
                                or ws[len(ws)-1] == "TriD" \
                                or ws[len(ws)-1] == "Dia":
                            color_string = l[:l.index("{} {} {}".format(
                                    ws[len(ws)-3], ws[len(ws)-2], ws[len(ws)-1]))]
                            fout.write(l)
                            l = fin.readline()
                            while l:
                                if l[0:12] == "% End plot #":
                                    fout.write(l)
                                    break
                                else:
                                    fout.write("{} {}".format(color_string, l))
                                    l = fin.readline()
                            break
                        else:
                            fout.write(l)
                            l = fin.readline()

                else:
                    fout.write(l)
                l = fin.readline()
            fin.close()
        fout.close()


    os.remove(fn)
    move(fntmp, fn)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("\nRequired argument: name of ps/eps file"
                    " to be edited.\n")
            quit()
        else:
            change_gnuplot_point_styles(sys.argv[1])
    else:
        raise RuntimeError("Please provide the ps/eps filename to be edited.")
