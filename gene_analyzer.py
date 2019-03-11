from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import ParsimonyTreeConstructor
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio.Phylo.TreeConstruction import ParsimonyScorer
from Bio import AlignIO



def create_tree(file_name):
    aln = AlignIO.read(file_name, 'phylip')
    print(aln)

    # Calculate the distance matrix
    calculator = DistanceCalculator('identity')
    dm = calculator.get_distance(aln)

    # Print the distance Matrix
    print('\nDistance Matrix\n===================')
    print(dm)

    # Construct the phylogenetic tree using UPGMA algorithm
    constructor = DistanceTreeConstructor()
    tree = constructor.upgma(dm)
    Phylo.write(tree, 'new.xml', 'phyloxml')

    # Draw the phylogenetic tree
    Phylo.draw(tree)

    # Print the phylogenetic tree in the terminal
    print('\nPhylogenetic Tree\n===================')
    Phylo.draw_ascii(tree)
