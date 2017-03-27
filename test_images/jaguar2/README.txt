In this dataset the source image has been split into four pieces and
rearranged to create the target image. Therefore the NNF should consist
of four regions each of whose vectors are identical and point to the new 
location of each piece. 

0. For the starter code to run, you must first complete the image
   reading/writing functions in patchMatch.py

1. To create an initial NNF that you can use repeatedly (for predictable
   algorithm operation):

cd ../../code
python viscomp.py --source ../test_images/jaguar2/source.png --target ../test_images/jaguar2/target.png --nnf-image --nnf-vectors --iters 0 --output ../results/jaguar2/jaguar2
mv ../results/jaguar2/jaguar2.*.npy ../results/jaguar2/jaguar2.init.npy

2. To test your reconstruct_source_from_target() function without having
   implemented the rest of the algorithm, run the starter code using
   the reference-computed NNF as your initial NNF:

cd ../../code
python viscomp.py --source ../test_images/jaguar2/source.png --target ../test_images/jaguar2/target.png --init-nnf ../results/jaguar2/jaguar2.reference.npy -iters 0 --rec-source --output ../results/jaguar2/jaguar2

3. To run patchmatch with the suggested parameters, your previously-computed
   initial NNF, and all intermediate results:

cd ../../code
python viscomp.py --source ../test_images/jaguar2/source.png --target ../test_images/jaguar2/target.png --init-nnf ../results/jaguar2/jaguar2.init.npy -iters 5 --partial-results --nnf-image --nnf-vectors --rec-source --output ../test_images/jaguar2/jaguar2

The above assumes you have already implemented the 
reconstruct_source_from_target() function. If you haven't, you should 
remove --rec-source from the above command

4. See file TIMINGS.txt which shows the execution time of the reference
implementation on CDF for the above command line


# canyon
python viscomp.py --source ../test_images/canyon/source.jpg --target ../test_images/canyon/target.jpg --nnf-image --nnf-vectors --iters 0 --output ../results/canyon/canyon
mv ../results/canyon/canyon.*.npy ../results/canyon/canyon.init.npy
python viscomp.py --source ../test_images/canyon/source.jpg --target ../test_images/canyon/target.jpg --init-nnf ../results/canyon/canyon.init.npy -iters 5 --partial-results --nnf-image --nnf-vectors --rec-source --output ../test_images/canyon/canyon

# deer
python viscomp.py --source ../test_images/deer/source.png --target ../test_images/deer/target.png --nnf-image --nnf-vectors --iters 0 --output ../results/deer/deer
mv ../results/deer/deer.*.npy ../results/deer/deer.init.npy
python viscomp.py --source ../test_images/deer/source.png --target ../test_images/deer/target.png --init-nnf ../results/deer/deer.init.npy -iters 5 --partial-results --nnf-image --nnf-vectors --rec-source --output ../test_images/deer/deer

# jaguar
python viscomp.py --source ../test_images/jaguar/source.png --target ../test_images/jaguar/target.png --nnf-image --nnf-vectors --iters 0 --output ../results/jaguar/jaguar
mv ../results/jaguar/jaguar.*.npy ../results/jaguar/jaguar.init.npy
python viscomp.py --source ../test_images/jaguar/source.png --target ../test_images/jaguar/target.png --init-nnf ../results/jaguar/jaguar.init.npy -iters 5 --partial-results --nnf-image --nnf-vectors --rec-source --output ../test_images/jaguar/jaguar

# jaguar2
python viscomp.py --source ../test_images/jaguar2/source.png --target ../test_images/jaguar2/target.png --nnf-image --nnf-vectors --iters 0 --output ../results/jaguar2/jaguar2
mv ../results/jaguar2/jaguar2.*.npy ../results/jaguar2/jaguar2.init.npy
python viscomp.py --source ../test_images/jaguar2/source.png --target ../test_images/jaguar2/target.png --init-nnf ../results/jaguar2/jaguar2.init.npy -iters 5 --partial-results --nnf-image --nnf-vectors --rec-source --output ../test_images/jaguar2/jaguar2

# jaguar3
python viscomp.py --source ../test_images/jaguar3/source.png --target ../test_images/jaguar3/target.png --nnf-image --nnf-vectors --iters 0 --output ../results/jaguar3/jaguar3
mv ../results/jaguar/jaguar.*.npy ../results/jaguar/jaguar.init.npy
python viscomp.py --source ../test_images/jaguar3/source.png --target ../test_images/jaguar3/target.png --init-nnf ../results/jaguar3/jaguar3.init.npy -iters 5 --partial-results --nnf-image --nnf-vectors --rec-source --output ../test_images/jaguar3/jaguar3