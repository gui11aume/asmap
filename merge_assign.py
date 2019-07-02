#/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import sys

from p2fcoord import p2findex

def print_out(buf, idx, tag=None):
   for line in buf:
      items = line.split()
      chrom = items[2]
      refchrom = re.sub(r'[^.]+$', 'ref', chrom)
      pos = int(items[3])
      refpos = idx.switchcoord(chrom, refchrom, pos)
      items[2] = refchrom
      items[3] = str(refpos)
      ztag = '\tZZ:Z:' + tag if tag else '\tZZ:Z:' + chrom
      sys.stdout.write('\t'.join(items) + ztag + '\n')

def output(buff, bufg, readname, idx):
   # There seems to be no way to suppress multi-line output
   # in BWA, so we need to filter them in the output file.
   if len(buff) != len(bufg):
      return
   if not bufg[0].startswith(readname):
      raise Exception
   # Mapping quality 0 means repeat.
   isrepeatf = sum([int(line.split()[4]) for line in buff]) == 0
   isrepeatg = sum([int(line.split()[4]) for line in bufg]) == 0
   if isrepeatf and isrepeatg:
      return print_out(buff, idx, 'rep')
   # At least partially mapped in one genome.
   # Choose which to output based on alignment score.
   scoref = scoreg = 0
   for line in buff:
      (score,) = re.search(r'AS:i:(\d+)', line).groups()
      scoref += int(score)
   for line in bufg:
      (score,) = re.search(r'AS:i:(\d+)', line).groups()
      scoreg += int(score)
   if scoref > scoreg:
      return print_out(buff, idx)
   if scoreg > scoref:
      return print_out(bufg, idx)
   else:
      return print_out(buff, idx, 'amb')



def main(f, g, idx):
   # Skip headers.
   for linef in f:
      if not linef.startswith('@'): break
   for lineg in g:
      if not lineg.startswith('@'): break

   # Zip the files.
   buff = [linef]
   bufg = [lineg]
   readname = linef.split()[0]
   for linef in f:
      if linef.startswith(readname):
         buff += [linef]
      else:
         for lineg in g:
            if lineg.startswith(readname):
               bufg += [lineg]
            else:
               break
         output(buff, bufg, readname, idx)
         readname = linef.split()[0]
         buff = [linef]
         bufg = [lineg]
   # Last read.
   for lineg in g:
      if lineg.startswith(readname):
         bufg += [lineg]
   output(buff, bufg, readname, idx)

if __name__ == '__main__':
   idx = p2findex.create_from_p2f_files(sys.argv[3:])
   with open(sys.argv[1]) as f, open(sys.argv[2]) as g:
      main(f, g, idx)
