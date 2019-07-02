SHELL= bash
TARGETS= \
	 6NG3.mrg.sam.gz \
	 6NN4.mrg.sam.gz \
	 7NN3.mrg.sam.gz \
	 8NN1.mrg.sam.gz \
	 6NM4.mrg.sam.gz \
	 7NG3.mrg.sam.gz \
	 8NG1.mrg.sam.gz \
	 8NN2.mrg.sam.gz \
	 6NN3.mrg.sam.gz \
	 7NG4.mrg.sam.gz \
	 8NG2.mrg.sam.gz

BWA= /mnt/shared/bin/bwa
CASBWA= /mnt/shared/seq/bwa/cas/cas.fa
MUSBWA= /mnt/shared/seq/bwa/mus/mus.fa

# Options for Hi-C
# BWAOPT= mem -t4 -P -k17 -U0 -L0,0 -T25
BWAOPT= mem -t4 -L500

all: $(TARGETS)

# Align with bwa (in two genomes).
%.cas.bam: %_*.fastq.gz
	$(BWA) $(BWAOPT) $(CASBWA) $? | \
		samtools view -b - | \
		samtools fixmate -@4 -m - $@
%.mus.bam: %_*.fastq.gz
	$(BWA) $(BWAOPT) $(MUSBWA) $? | \
		samtools view -b - | \
		samtools fixmate -@4 -m - $@

# Merge.
%.mrg.sam.gz: %.cas.bam %.mus.bam
	python merge_assign.py \
		$(foreach f, $?, <(samtools view -h $(f))) p2f/* | gzip > $@
