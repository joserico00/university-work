import csv
import re

def moods_csv_to_bed(input_csv, output_bed):
    #porfavoe que termine todo los pfm con el numero en # #bp.pfm
    pattern = r"(\d+)bp\.pfm$"
    color = {}
    color["Nkx2-5Tbx5_019_monNKX_edit6bp.pfm"]=[102,204,255]
    color["Nkx2-5Tbx5_019_monTBX_edit6bp.pfm"]=[255,153,153]
    color["Nkx2-5Tbx5_019_seed1_edit12bp.pfm"]=[153, 51,255]
    color["Nkx2-5Tbx5_019_seed2_edit17bp.pfm"]=[153,102,255]
    color["Nkx2-5Tbx5_019_seed3_edit19bp.pfm"]=[153,153,255]
    
    
    
    
    
    with open(input_csv, 'r') as moods_csv:
        csv_reader = csv.reader(moods_csv, delimiter=',')
        
        with open(output_bed, 'w') as bed_file:
            starting = 'browser position chr1:1-1000\ntrack name="moods_hits2" description="MOODS hits" visibility=2 itemRgb="On"\n'
            bed_file.write(starting)
            for row in csv_reader:
                chrom_info = row[0].split(':')
                chrom_range = chrom_info[1].split('-')

                chromosome = chrom_info[0]
                start = chrom_range[0]
                end = chrom_range[1]
                name = row[1]
                match = re.search(pattern, name)
                number = int(match.group(1))
                strand = row[3]
                score = row[4]
                Dna= row[5]
                rgb=color[name]
                rgbstr=', '.join(map(str, rgb))
                hitposition=row[2]
                hitstart=int(chrom_range[0])+int(row[2])
                thickStart=0
                thickEnd=0
                #hitend que es el nombre de files sumado a hitstart
                hitend=hitstart+number
                #bed_line = f"{chromosome}\t{start}\t{end}\t{name}\t{score}\t{strand}\t{hitposition}\t{hitstart}\t{hitend}\t{Dna}\n"
                #bed_line = f"{chromosome}\t{hitstart}\t{hitend}\t{name}\t{score}\t{strand}\t{hitposition}\t{start}\t{end}\t{rgbstr}\t{Dna}\n"
                #bed_line = f"{chromosome}\t{hitstart}\t{hitend}\t{name}\t{score}\t{strand}\t{thickStart}\t{thickEnd}\t{rgbstr}\n"
                #bed_line = bed_line = f"{chromosome}\t{start}\t{end}\t{name}\t{score}\t{strand}\t{hitstart}\t{hitend}\t{rgb[0]},{rgb[1]},{rgb[2]}\n"
                bed_line = bed_line = f"{chromosome}\t{hitstart}\t{hitend}\t{name}\t{score}\t{strand}\t{thickStart}\t{thickEnd}\t{rgb[0]},{rgb[1]},{rgb[2]}\n"
                bed_file.write(bed_line)


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_csv output_bed")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_bed = sys.argv[2]

    moods_csv_to_bed(input_csv, output_bed)

