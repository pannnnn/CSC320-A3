# CSC320 Winter 2017
# Assignment 3
# (c) Olga (Ge Ya) Xu, Kyros Kutulakos
#
# DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
# AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION
# BY KYROS KUTULAKOS IS STRICTLY PROHIBITED. VIOLATION OF THIS
# POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

#
# DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
#

# import basic packages
import numpy as np
import random

# basic numpy configuration

# set random seed
np.random.seed(seed=131)
# ignore division by zero warning
np.seterr(divide='ignore', invalid='ignore')


# This function implements the basic loop of the PatchMatch
# algorithm, as explained in Section 3.2 of the paper.
# The function takes an NNF f as input, performs propagation and random search,
# and returns an updated NNF.
#
# The function takes several input arguments:
#     - source_patches:      The matrix holding the patches of the source image,
#                            as computed by the make_patch_matrix() function. For an
#                            NxM source image and patches of width P, the matrix has
#                            dimensions NxMxCx(P^2) where C is the number of color channels
#                            and P^2 is the total number of pixels in the patch. The
#                            make_patch_matrix() is defined below and is called by the
#                            initialize_algorithm() method of the PatchMatch class. For
#                            your purposes, you may assume that source_patches[i,j,c,:]
#                            gives you the list of intensities for color channel c of
#                            all pixels in the patch centered at pixel [i,j]. Note that patches
#                            that go beyond the image border will contain NaN values for
#                            all patch pixels that fall outside the source image.
#     - target_patches:      The matrix holding the patches of the target image.
#     - f:                   The current nearest-neighbour field
#     - alpha, w:            Algorithm parameters, as explained in Section 3 and Eq.(1)
#     - propagation_enabled: If true, propagation should be performed.
#                            Use this flag for debugging purposes, to see how your
#                            algorithm performs with (or without) this step
#     - random_enabled:      If true, random search should be performed.
#                            Use this flag for debugging purposes, to see how your
#                            algorithm performs with (or without) this step.
#     - odd_iteration:       True if and only if this is an odd-numbered iteration.
#                            As explained in Section 3.2 of the paper, the algorithm
#                            behaves differently in odd and even iterations and this
#                            parameter controls this behavior.
#     - best_D:              And NxM matrix whose element [i,j] is the similarity score between
#                            patch [i,j] in the source and its best-matching patch in the
#                            target. Use this matrix to check if you have found a better
#                            match to [i,j] in the current PatchMatch iteration
#     - global_vars:         (optional) if you want your function to use any global variables,
#                            you can pass them to/from your function using this argument

# Return arguments:
#     - new_f:               The updated NNF
#     - best_D:              The updated similarity scores for the best-matching patches in the
#                            target
#     - global_vars:         (optional) if you want your function to use any global variables,
#                            return them in this argument and they will be stored in the
#                            PatchMatch data structure


def propagation_and_random_search(source_patches, target_patches,
                                  f, alpha, w,
                                  propagation_enabled, random_enabled,
                                  odd_iteration, best_D=None,
                                  global_vars=None
                                ):
    new_f = f.copy()

    #############################################
    ###  PLACE YOUR CODE BETWEEN THESE LINES  ###
    #############################################
    row = source_patches.shape[0]
    column = source_patches.shape[1]

    # calculate how many random search offset we need
    i = 0
    while(w * alpha ** i >= 1):
                i += 1
    while_iters = i

    # initialize array_for_random_offset to accelerate comparison in random search 
    array_for_random_offset = np.zeros((1,while_iters+1,2)).astype(int)

    # initialize algorithm properties
    random_enabled = True
    propagation_enabled = True
    source_patches = np.nan_to_num(source_patches)
    target_patches = np.nan_to_num(target_patches)    

    # make ordered index of the image
    source_index = make_coordinates_matrix(source_patches.shape)

    # varible whose name includes 'window' stores the array of pixels we need to compare      
    # scan along the width and then the height, all pixels in each diagonal is manipulated
    # in one single loop
    if odd_iteration:
        for i in range(column+row-1):
            # calculate diagonal index
            if(i<column):
                diagonal_length = min(i+1,row)
                x = np.arange(i, max(-1, i-row), -1)
                y = (x[::-1]%row)
                y.sort()
            else:
                diagonal_length = column + row - i - 1
                x = np.arange(column-1, column-1-diagonal_length , -1)
                y = np.arange(row-diagonal_length,row,1)
            diagonal_index = np.dstack((y, x)).reshape((diagonal_length,2))

            # Propogation
            if propagation_enabled:
                # if first pixel of the image, nothing to compare with
                if(i==0):
                    continue

                # calculate left neighbor index
                left_neighbor_index = np.copy(diagonal_index)
                left_neighbor_index[:,0] = diagonal_index[:,0]-1
                temp = left_neighbor_index[:,0]
                temp[temp<0] = 0
                left_neighbor_index[:,0] = temp

                # calculate top neighbor index
                top_neighbor_index = np.copy(diagonal_index)
                top_neighbor_index[:,1] = diagonal_index[:,1]-1
                temp = top_neighbor_index[:,1]
                temp[temp<0] = 0
                top_neighbor_index[:,1] = temp

                # initialize source image and target image index for density calculation
                source_window_index = np.stack((diagonal_index, top_neighbor_index, left_neighbor_index), axis = 1)
                window_f = new_f[source_window_index[:,:,0],source_window_index[:,:,1]]
                target_window_index = source_window_index + window_f
                
                # clip the index afte adding offset to its boundaries
                target_window_x = np.clip(target_window_index[:,:,0],0,row-1)
                target_window_y = np.clip(target_window_index[:,:,1],0,column-1)
                source_window = source_patches[source_window_index[:,:,0],source_window_index[:,:,1]]
                target_window = target_patches[target_window_x,target_window_y]

                # calculate the difference in density of those pixels
                window_D = np.sum(np.sum((target_window - source_window)**2, axis = 3), axis = 2)

                # update the offset per pixel if better result is found
                min_index = np.argmin(window_D,axis=1)
                x = source_window_index[:,0,0]
                y = source_window_index[:,0,1]
                new_f[x, y] = window_f[np.arange(diagonal_length),min_index]

            # Random Search
            if random_enabled:
                # store search radius in array_for_random_offset, first spot is center of the search region 
                j = 1
                while(j < while_iters+1):
                        cur_R = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
                        array_for_random_offset[0,j,:] = w * alpha ** j * cur_R
                        j +=1

                # populate the offset array for comparison
                source_window_index = np.repeat(diagonal_index.reshape(diagonal_length,1,2), while_iters+1, axis = 1)
                random_offset = np.repeat(array_for_random_offset, diagonal_length, axis=0)          
                window_f = random_offset + new_f[source_window_index[:,:,0],source_window_index[:,:,1]]
                # clip the index afte adding offset to its boundaries
                target_window_x = np.clip((source_window_index + window_f)[:,:,0],0,row-1)
                target_window_y = np.clip((source_window_index + window_f)[:,:,1],0,column-1)
                # correct the offset array such that after adding offset no pixels will potentially cross the 
                # boundaries
                window_f[:,:,0] = target_window_x - source_window_index[:,:,0]
                window_f[:,:,1] = target_window_y - source_window_index[:,:,1]
                source_window = source_patches[source_window_index[:,:,0],source_window_index[:,:,1]]
                target_window = target_patches[target_window_x,target_window_y]
                # calculate the difference in density of those pixels
                window_D = np.sum(np.sum((target_window - source_window)**2, axis = 3), axis = 2)
                # update the offset per pixel if better result is found
                min_index = np.argmin(window_D,axis=1)
                x = source_window_index[:,0,0]
                y = source_window_index[:,0,1]
                new_f[x, y] = window_f[np.arange(diagonal_length),min_index]
    # scan in reversed order
    else:
        for i in range(column+row-2,-1,-1):
            # calculate diagonal index
            if(i<column):
                diagonal_length = min(i+1,row)
                x = np.arange(i, max(-1, i-row), -1)
                y = (x[::-1]%row)
                y.sort()
            else:
                diagonal_length = column + row - i - 1
                x = np.arange(column-1, column-1-diagonal_length , -1)
                y = np.arange(row-diagonal_length,row,1)
            diagonal_index = np.dstack((y, x)).reshape((diagonal_length,2))

            # Propogation
            if propagation_enabled:
                # if last pixel of the image, nothing to compare with
                if(i==column+row-2):
                    continue

                # calculate right neighbor index
                right_neighbor_index = np.copy(diagonal_index)
                right_neighbor_index[:,0] = diagonal_index[:,0]+1
                temp = right_neighbor_index[:,0]
                temp[temp>=row] = row-1
                right_neighbor_index[:,0] = temp

                # calculate bottom neighbor index
                bottom_neighbor_index = np.copy(diagonal_index)
                bottom_neighbor_index[:,1] = diagonal_index[:,1]+1
                temp = bottom_neighbor_index[:,1]
                temp[temp>=column] = column-1
                bottom_neighbor_index[:,1] = temp

                # initialize source image and target image index for density calculation
                source_window_index = np.stack((diagonal_index, bottom_neighbor_index, right_neighbor_index), axis = 1)
                window_f = new_f[source_window_index[:,:,0],source_window_index[:,:,1]]
                target_window_index = source_window_index + window_f

                # clip the index afte adding offset to its boundaries
                target_window_x = np.clip(target_window_index[:,:,0],0,row-1)
                target_window_y = np.clip(target_window_index[:,:,1],0,column-1)
                source_window = source_patches[source_window_index[:,:,0],source_window_index[:,:,1]]
                target_window = target_patches[target_window_x,target_window_y]

                # calculate the difference in density of those pixels
                window_D = np.sum(np.sum((target_window - source_window)**2, axis = 3), axis = 2)
                
                # update the offset per pixel if better result is found
                min_index = np.argmin(window_D,axis=1)
                x = source_window_index[:,0,0]
                y = source_window_index[:,0,1]
                new_f[x, y] = window_f[np.arange(diagonal_length),min_index]

            # Random Search
            if random_enabled:
                # store search radius in array_for_random_offset, first spot is center of the search region 
                j = 1
                while(j < while_iters+1):
                        cur_R = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
                        array_for_random_offset[0,j,:] = w * alpha ** j * cur_R
                        j +=1
                        
                # populate the offset array for comparison
                source_window_index = np.repeat(diagonal_index.reshape(diagonal_length,1,2), while_iters+1, axis = 1)
                random_offset = np.repeat(array_for_random_offset, diagonal_length, axis=0)          
                window_f = random_offset + new_f[source_window_index[:,:,0],source_window_index[:,:,1]]
                # clip the index afte adding offset to its boundaries
                target_window_x = np.clip((source_window_index + window_f)[:,:,0],0,row-1)
                target_window_y = np.clip((source_window_index + window_f)[:,:,1],0,column-1)
                # correct the offset array such that after adding offset no pixels will potentially cross the 
                # boundaries
                window_f[:,:,0] = target_window_x - source_window_index[:,:,0]
                window_f[:,:,1] = target_window_y - source_window_index[:,:,1]
                source_window = source_patches[source_window_index[:,:,0],source_window_index[:,:,1]]
                target_window = target_patches[target_window_x,target_window_y]
                # calculate the difference in density of those pixels
                window_D = np.sum(np.sum((target_window - source_window)**2, axis = 3), axis = 2)
                # update the offset per pixel if better result is found
                min_index = np.argmin(window_D,axis=1)
                x = source_window_index[:,0,0]
                y = source_window_index[:,0,1]
                new_f[x, y] = window_f[np.arange(diagonal_length),min_index]
                    
    #############################################

    return new_f, best_D, global_vars


# This function uses a computed NNF to reconstruct the source image
# using pixels from the target image. The function takes two input
# arguments
#     - target: the target image that was used as input to PatchMatch
#     - f:      the nearest-neighbor field the algorithm computed
# and should return a reconstruction of the source image:
#     - rec_source: an openCV image that has the same shape as the source image
#
# To reconstruct the source, the function copies to pixel (x,y) of the source
# the color of pixel (x,y)+f(x,y) of the target.
#
# The goal of this routine is to demonstrate the quality of the computed NNF f.
# Specifically, if patch (x,y)+f(x,y) in the target image is indeed very similar
# to patch (x,y) in the source, then copying the color of target pixel (x,y)+f(x,y)
# to the source pixel (x,y) should not change the source image appreciably.
# If the NNF is not very high quality, however, the reconstruction of source image
# will not be very good.
#
# You should use matrix/vector operations to avoid looping over pixels,
# as this would be very inefficient

def reconstruct_source_from_target(target, f):
    rec_source = None

    #############################################
    ###  PLACE YOUR CODE BETWEEN THESE LINES  ###
    #############################################
    
    target_index = make_coordinates_matrix(target.shape) + f 
    x = np.clip(target_index[:,:,0],0,target.shape[0]-1)
    y = np.clip(target_index[:,:,1],0,target.shape[1]-1)
    rec_source = target[x, y]

    #############################################

    return rec_source


# This function takes an NxM image with C color channels and a patch size P
# and returns a matrix of size NxMxCxP^2 that contains, for each pixel [i,j] in
# in the image, the pixels in the patch centered at [i,j].
#
# You should study this function very carefully to understand precisely
# how pixel data are organized, and how patches that extend beyond
# the image border are handled.


def make_patch_matrix(im, patch_size):
    phalf = patch_size // 2
    # create an image that is padded with patch_size/2 pixels on all sides
    # whose values are NaN outside the original image
    padded_shape = im.shape[0] + patch_size - 1, im.shape[1] + patch_size - 1, im.shape[2]
    padded_im = np.zeros(padded_shape) * np.NaN
    padded_im[phalf:(im.shape[0] + phalf), phalf:(im.shape[1] + phalf), :] = im

    # Now create the matrix that will hold the vectorized patch of each pixel. If the
    # original image had NxM pixels, this matrix will have NxMx(patch_size*patch_size)
    # pixels
    patch_matrix_shape = im.shape[0], im.shape[1], im.shape[2], patch_size ** 2
    patch_matrix = np.zeros(patch_matrix_shape) * np.NaN
    for i in range(patch_size):
        for j in range(patch_size):
            patch_matrix[:, :, :, i * patch_size + j] = padded_im[i:(i + im.shape[0]), j:(j + im.shape[1]), :]

    return patch_matrix


# Generate a matrix g of size (im_shape[0] x im_shape[1] x 2)
# such that g(y,x) = [y,x]
#
# Step is an optional argument used to create a matrix that is step times
# smaller than the full image in each dimension
#
# Pay attention to this function as it shows how to perform these types
# of operations in a vectorized manner, without resorting to loops


def make_coordinates_matrix(im_shape, step=1):
    """
    Return a matrix of size (im_shape[0] x im_shape[1] x 2) such that g(x,y)=[y,x]
    """
    range_x = np.arange(0, im_shape[1], step)
    range_y = np.arange(0, im_shape[0], step)
    axis_x = np.repeat(range_x[np.newaxis, ...], len(range_y), axis=0)
    axis_y = np.repeat(range_y[..., np.newaxis], len(range_x), axis=1)

    return np.dstack((axis_y, axis_x))