import fuga as fu


a = fu.biome(num_species=5,species_num_fugues=100,fractions_of_parents=0.1,global_harmonic_references=0,local_harmonic_references=0,range_references=14,variability_references=22.5,variability_chords_per_bar_references=0.5,num_bar_references=7.5,ending_references=100,beginning_references=100)
a.converge_species(plot="yes")