def run_length_encode(S):
    """
    Run-Length Encoding (RLE) function.
    
    Input: String S of length n
    Output: Encoded string where consecutive identical characters are replaced
            with the count followed by the character.
    """
    if not S:
        return ""
    
    result = ""
    count = 1
    n = len(S)
    
    for i in range(1, n):
        if S[i] == S[i-1]:
            count += 1
        else:
            result += str(count) + S[i-1]
            count = 1
    
    # Append the last group
    result += str(count) + S[n-1]
    
    return result

# Example usage
input_string = "AABBC"
encoded = run_length_encode(input_string)
print(f"Original: {input_string}")
print(f"Encoded: {encoded}")
# Output:
# Original: WWWWWWWWWWWWBBB
# Encoded: 12W1B3W