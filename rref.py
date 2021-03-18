# a matrix is a list of lists
# all matrix functions in this code use 0 indexing, for convenience.
# when I print the operation out, I just add one to the indices.

# prevent ugly decimals
from fractions import Fraction

# R(m+1) <-> R(n+1)
def swap_rows(mat, m, n):
    assert(m != n) # sanity check
    t = mat[m]
    mat[m] = mat[n]
    mat[n] = t

# R(m+1) -> kR(m+1)
def multiply_row(mat, m, k):
    assert(k != 0) # sanity check
    columns = len(mat[m])
    for col in range(columns):
        mat[m][col] *= k

# R(m+1) -> R(m+1) + kR(n+1)
def add_multiple_of_row(mat, m, n, k):
    assert(m!=n)
    assert(k!=0)
    columns = len(mat[m])
    for col in range(columns):
        mat[m][col] += k * mat[n][col]

def frac_to_latex(f):
    "Converts the fraction f into its LaTeX representation"
    if f.denominator == 1:
        return str(f.numerator)
    elif f.numerator < 0:
        return "-\\frac{"+str(-f.numerator)+"}{"+str(f.denominator)+"}"
    else:
        return "\\frac{"+str(f.numerator)+"}{"+str(f.denominator)+"}"

def frac_to_coeff(f):
    "Converts the fraction f into a coefficient with a sign"
    if f == 1:
        return "+"
    if f == -1:
        return "-"
    if f.numerator < 0:
        return frac_to_latex(f)
    else:
        return "+" + frac_to_latex(f)

def format_matrix(mat, aug=0):
    "Converts the matrix mat into its LaTeX representation (aug specifies number of augmented matrix)"
    rows = len(mat)
    cols = len(mat[0])
    ans = "\\left[\\begin{array}{@{}%s@{}}\n" % ("c"*cols if aug == 0 else "c"*(cols-aug)+"|"+"r"*aug)
    for row in mat:
        ans += " & ".join(frac_to_latex(f) for f in row)
        ans += "\\\\\n"
    ans += "\\end{array}\\right]\n"
    return ans

def rref(mat, aug=0):
    """Performs Gauss-Jordan elimination to turn the matrix mat into RREF form in-place
and returns a string showing the working in LaTeX"""
    row = 0
    col = 0
    n_rows = len(mat)
    n_cols = len(mat[0])
    ans = "\\begin{align*}\n"
    while True:
        if(row >= n_rows): # ran out of rows, RREF done
            ans += "&" + format_matrix(mat, aug)
            break
        elif(col >= n_cols): # ran out of cols, RREF done
            ans += "&" + format_matrix(mat, aug)
            break
        elif(mat[row][col] != 0): # nonzero value
            if mat[row][col] != 1: # if value not 1, divide the row to make it 1
                recip = 1/mat[row][col]
                ans += "&" + format_matrix(mat, aug)
                ans += ("\\\\\n\\overset{%s R_{%d}}{\\longrightarrow}\n"
                        % (frac_to_latex(recip), row + 1))
                multiply_row(mat, row, recip)
            for r in range(n_rows): # make sure all other rows for that column are 0
                if r == row: # make sure to skip the same row
                    continue
                if mat[r][col] != 0:
                    ans += "&" + format_matrix(mat, aug)
                    ans += ("\\\\\n\\overset{R_{%d} %s R_{%d}}{\\longrightarrow}\n"
                            % (r+1, frac_to_coeff(-mat[r][col]), row + 1))
                    add_multiple_of_row(mat, r, row, -mat[r][col])
            row += 1
            col += 1
        else: # mat[row][col] == 0
            for r in range(row+1, n_rows):
                if mat[r][col] != 0:
                    ans += "&" + format_matrix(mat, aug)
                    ans += ("\\\\\n\\overset{R_{%d} \\leftrightarrow R_{%d}}{\\longrightarrow}\n"
                            % (r+1, row + 1))
                    swap_rows(mat, r, row)
                    break
            else: # basically, this is executed if we don't break
                col += 1
    return ans+ "\\end{align*}"

def fractionize_matrix(mat):
    return [[Fraction(x) for x in row] for row in mat]

def main():
    print("Matrix RREF calculator\n")
    rows = int(input("Number of rows: "))
    cols = int(input("Number of cols: "))
    if (rows <= 0 or cols <= 0):
        print("Please enter valid numbers.")
        return
    print("\nEnter your matrix numbers in order (separated by a space, fractions like a/b ok):\n")
    m = []
    for i in range(rows):
        r = input("Enter row {}: ".format(i+1))
        r = r.split(" ")
        if(len(r) != cols):
            print("Wrong number of columns.")
            return
        m.append([Fraction(s) for s in r])
    temp = input("Is your matrix an augmented matrix? [yn] ")
    if temp[0].lower() == "y":
        aug = int(input("Enter number of augmented columns:"))
    else:
        aug = 0
    print("\n==LATEX OUTPUT==\n")
    print(rref(m, aug))
                    
                
if __name__ == "__main__":
    main()
