#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import sys

from bisect import bisect_left, bisect_right

class GapLessBlock:
   '''
   Coordinates of alignment without gaps between genomes.
   Blocks have the 4 following attributes:
      s1: block start in first genome
      e1: block end in first genome
      s2: block start in second genome
      e2: block end in second genome

   The class implements comparisons with __lt__ and __gt__.
   The < operator compares numbers to e1, and the > operator
   compares numbers to e2. Since 'bisect_left' uses __lt__
   and 'bisect_right' uses __gt__, this gives a way to look
   for a block in genome 1 or genome 2 by changing the bisection
   method.
   '''
   def __init__(self, s1, e1, s2, e2):
      self.s1 = s1
      self.e1 = e1
      self.s2 = s2
      self.e2 = e2

   def __lt__(self, other):
      return self.e1 < other

   def __gt__(self, other):
      return self.e2 > other

   def boundaries(self):
      return (self.s1, self.e1, self.s2, self.e2)


class SeqPair:
   def __init__(self, seqname1, seqname2):
      self.seqname1 = seqname1 # Genome 1 (order matters).
      self.seqname2 = seqname2 # Genome 2 (order matters).
      self.blocks = list()

   def append(self, block):
      self.blocks.append(block)


class p2findex:

   def __init__(self):
      self.seqnames = dict()

   @staticmethod
   def create_from_p2f_files(list_of_names):
      idx = p2findex()
      for fname in list_of_names:
         name2 = re.sub(r'.p2f$', '', os.path.basename(fname))
         name1 = re.sub(r'[^.]+$', 'ref', name2)
         with open(fname) as f:
            idx.add_from_p2f_file(f, name1, name2)
      return idx

   def add_from_p2f_file(self, f, name1, name2):
      # Create data structure.
      pair = SeqPair(name1, name2)
      self.seqnames[frozenset([name1,name2])] = pair
      s1 = 1
      s2 = 1
      shift = 0
      for line in f:
         e1,_,delta,_,sz = line.split()
         if delta == '0': continue # SNP
         e1 = int(e1)
         delta = int(delta)
         # Update end pointer.
         shift += delta
         e2 = e1 + shift
         # Store block.
         pair.append(GapLessBlock(s1,e1,s2,e2))
         # Update start pointers.
         s1 = e1
         s2 = e2
      # Add final bit.
      e1 = s1 + int(sz)
      e2 = s2 + int(sz)
      pair.append(GapLessBlock(s1,e1,s2,e2))

   def switchcoord(self, source, dest, pos):
      try:
         pair = self.seqnames[frozenset([source,dest])]
         if source == pair.seqname1:
            # We need to search genome 1.
            i = bisect_left(pair.blocks, pos)
            block = pair.blocks[i]
            s1,e1, s2,e2 = block.boundaries()
            if s1 <= pos <= e1:
               return s2 + (pos-s1)
         elif source == pair.seqname2:
            # We need to search genome 2.
            i = bisect_right(pair.blocks, pos)
            block = pair.blocks[i]
            s1,e1, s2,e2 = block.boundaries()
            if s2 <= pos <= e2:
               return s1 + (pos-s2)
      except (KeyError, IndexError):
         return float('nan')


