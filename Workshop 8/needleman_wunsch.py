def align(seq1, seq2, gap_penalty=-1, match_score=1, mismatch_penalty=-1, width=70):
    """Performs global sequence alignment using the Needleman-Wunsch algorithm.

    Args:
        seq1 (str): First sequence to align.
        seq2 (str): Second sequence to align.
        gap_penalty (int, optional): Penalty score for a gap. Defaults to -1.
        match_score (int, optional): Score for a matching nucleotide. Defaults to 1.
        mismatch_penalty (int, optional): Penalty score for a mismatched nucleotide. Defaults to -1.

    Returns:
        tuple: Tuple containing the aligned sequences, the alignment score, and the formatted output.
    """
    # Initialize the scoring matrix.
    n = len(seq1)
    m = len(seq2)
    score_matrix = [[0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(1, n + 1):
        score_matrix[i][0] = gap_penalty * i
    for j in range(1, m + 1):
        score_matrix[0][j] = gap_penalty * j

    # Fill in the scoring matrix.
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = score_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_penalty)
            delete = score_matrix[i - 1][j] + gap_penalty
            insert = score_matrix[i][j - 1] + gap_penalty
            score_matrix[i][j] = max(match, delete, insert)

    # Traceback to get the aligned sequences.
    align1 = ''
    align2 = ''
    i, j = n, m
    while i > 0 and j > 0:
        if score_matrix[i][j] == score_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_penalty):
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2
            i -= 1
            j -= 1
        elif score_matrix[i][j] == score_matrix[i - 1][j] + gap_penalty:
            align1 = seq1[i - 1] + align1
            align2 = '-' + align2
            i -= 1
        else:
            align1 = '-' + align1
            align2 = seq2[j - 1] + align2
            j -= 1

    # Add any remaining characters.
    while i > 0:
        align1 = seq1[i - 1] + align1
        align2 = '-' + align2
        i -= 1
    while j > 0:
        align1 = '-' + align1
        align2 = seq2[j - 1] + align2
        j -= 1
    # Format the output.
    alignment = ''
    id_line1 = 'seq1: '
    id_line2 = 'seq2: '
    matches = '      '
    for i in range(0, len(align1), width):
        seq1_slice = align1[i:i+width]
        seq2_slice = align2[i:i+width]
        match_slice = ''
        for j in range(len(seq1_slice)):
            if seq1_slice[j] == seq2_slice[j]:
                match_slice += '|'
            else:
                match_slice += ' '
        alignment += id_line1 + seq1_slice + '\n'
        alignment += matches + match_slice + '\n'
        alignment += id_line2 + seq2_slice + '\n\n'
    return alignment