
def create_orientation_list(maximum_value, division_value, 
                            length_list):
    '''
    This function creates all the possible orientations required by the user. 
    The orientations will be used to modify the reference orientation of the 
    stimulus grating set by the user and are stored in a list.
    
    Parameters
    ----------
    maximum_value : float
        The biggest difference between the reference orientation and the shown
        orientation of the stimulus grating.
    division_value : float
        The divisor between two adjacent orientations.
    length_list : int
        The total amount of orientations required by the user.

    Returns
    -------
    List[float]
        A list containing all the orientations required by the user to modify
        the reference orientation of the stimulus grating. The orientations are
        sorted in a descending order.

    '''
    orientation_list = [round(float(maximum_value)/(float(division_value)**
                                                    float(x)), 3) 
                        if x != 0 else float(maximum_value) for x in 
                        range(0, length_list)]
    
    return orientation_list


def create_contrast_list(maximum_value, division_value, 
                            length_list):
    '''
    This function creates all the possible contrasts required by the user. 
    The contrasts will be used to modify the reference contrast of the 
    stimulus grating set by the user and are stored in a list.
    
    Parameters
    ----------
    maximum_value : float
        The biggest difference between the reference contrast and the shown
        contrast of the stimulus grating.
    division_value : float
        The divisor between two adjacent contrasts.
    length_list : int
        The total amount of contrasts required by the user.

    Returns
    -------
    List[float]
        A list containing all the contrasts required by the user to modify
        the reference contrast of the stimulus grating. The contrasts are
        sorted in a descending order.
 
    '''
    contrast_list = [round(float(maximum_value)/(float(division_value)**
                                                    float(x)), 3) 
                        if x != 0 else float(maximum_value) for x in 
                        range(0, length_list)]
    
    return contrast_list
    
if __name__ == '__main__':
    create_orientation_list()