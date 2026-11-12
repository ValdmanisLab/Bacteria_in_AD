import pysam
import os
from collections import defaultdict


# ===============================
# USER SETTINGS
# ===============================

alignment_dir = os.path.dirname(os.path.abspath(__file__))
area_of_search = None   # Example: 'chr19:44903796-44911393'


# ===============================
# FUNCTIONS
# ===============================

def determine_chromosome_format(alignment_file):

    try:
        with pysam.AlignmentFile(alignment_file, 'rb') as align:

            for read in align:

                if read.reference_name != '*':
                    if read.reference_name.startswith('chr'):
                        return 'chr'
                    else:
                        return ''

    except Exception as e:
        print(f"Error reading alignment file {alignment_file}: {e}")

    return ''


def is_perfect_match(cigar):

    return len(cigar) == 1 and cigar[0][0] == 0


def find_patterns_in_alignment(alignment_file, area_of_search=None):

    patterns_found = []
    gap_sizes = []
    reads_with_pattern = []

    chrom_prefix = determine_chromosome_format(alignment_file)

    if area_of_search is not None:

        chrom, pos_range = area_of_search.split(':')

        chrom = chrom.replace('chr', chrom_prefix)

        start, end = map(int, pos_range.split('-'))

    else:

        chrom = None
        start = end = None

    try:

        with pysam.AlignmentFile(alignment_file, 'rb') as align:

            for read in align:

                if read.is_unmapped:
                    continue

                if chrom and (read.reference_name != chrom or
                              read.reference_start < start or
                              read.reference_end > end):
                    continue

                cigar = read.cigar

                if cigar is None:
                    continue

                # --------------------------------
                # Remove perfectly matched reads
                # --------------------------------
                if is_perfect_match(cigar):
                    continue

                if len(cigar) < 3:
                    continue

                seg_a = cigar[0]
                seg_b = cigar[1]
                seg_c = cigar[2]

                # --------------------------------
                # Pattern: M 24–1533 N M
                # --------------------------------
                if (seg_a[0] == 0 and
                    seg_b[0] == 3 and 24 <= seg_b[1] <= 1533 and
                    seg_c[0] == 0):

                    # Exclude canonical intron
                    if seg_b[1] == 580:
                        continue

                    patterns_found.append(
                        (read.query_name,
                         read.reference_name,
                         read.reference_start,
                         read.reference_end,
                         read.query_sequence)
                    )

                    gap_sizes.append(seg_b[1])
                    reads_with_pattern.append(read)

    except Exception as e:

        print(f"Error processing alignment file {alignment_file}: {e}")

    return patterns_found, gap_sizes, reads_with_pattern


# ===============================
# WRITE OUTPUT FILES
# ===============================

def write_fasta_and_bam(reads_with_pattern, alignment_file, output_dir):

    file_base = os.path.basename(alignment_file)

    fasta_path = os.path.join(output_dir, file_base.replace('.bam', '_reads_with_pattern.fa'))
    bam_output_path = os.path.join(output_dir, file_base.replace('.bam', '_reads_with_pattern.bam'))

    with pysam.AlignmentFile(alignment_file, 'rb') as align_in, \
         pysam.AlignmentFile(bam_output_path, 'wb', header=align_in.header) as bam_out, \
         open(fasta_path, 'w') as fasta_out:

        for read in reads_with_pattern:

            bam_out.write(read)

            fasta_out.write(
                f">{read.query_name} {read.reference_name}:{read.reference_start}-{read.reference_end}\n"
            )

            fasta_out.write(f"{read.query_sequence}\n")

    sorted_bam = bam_output_path.replace(".bam", ".sorted.bam")

    pysam.sort("-o", sorted_bam, bam_output_path)
    pysam.index(sorted_bam)

    os.remove(bam_output_path)


# ===============================
# MAIN PROCESSING LOOP
# ===============================

def process_directory(alignment_dir, area_of_search=None):

    for alignment_file in os.listdir(alignment_dir):

        if alignment_file.endswith(".bam") and not alignment_file.startswith("._"):

            alignment_file_path = os.path.join(alignment_dir, alignment_file)

            output_dir = os.path.join(
                alignment_dir,
                os.path.splitext(alignment_file)[0]
            )

            os.makedirs(output_dir, exist_ok=True)

            patterns_found, gap_sizes, reads_with_pattern = find_patterns_in_alignment(
                alignment_file_path,
                area_of_search
            )

            # Write outputs
            write_fasta_and_bam(reads_with_pattern, alignment_file_path, output_dir)

            # Print summary
            print(f"{alignment_file} : {len(reads_with_pattern)} reads passed filtering")


# ===============================
# RUN
# ===============================

process_directory(alignment_dir, area_of_search)
