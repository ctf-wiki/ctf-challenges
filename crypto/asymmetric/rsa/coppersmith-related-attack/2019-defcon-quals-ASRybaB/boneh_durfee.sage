import time
from ast import literal_eval
from multiprocessing import Pool
############################################
# Config
##########################################

"""
Setting debug to true will display more informations
about the lattice, the bounds, the vectors...
"""
debug = 0

"""
Setting strict to true will stop the algorithm (and
return (-1, -1)) if we don't have a correct
upperbound on the determinant. Note that this
doesn't necesseraly mean that no solutions
will be found since the theoretical upperbound is
usualy far away from actual results. That is why
you should probably use `strict = False`
"""
strict = False

"""
This is experimental, but has provided remarkable results
so far. It tries to reduce the lattice as much as it can
while keeping its efficiency. I see no reason not to use
this option, but if things don't work, you should try
disabling it
"""
helpful_only = True
dimension_min = 7 # stop removing if lattice reaches that dimension

############################################
# Functions
##########################################

# display stats on helpful vectors
def helpful_vectors(BB, modulus):
    nothelpful = 0
    for ii in range(BB.dimensions()[0]):
        if BB[ii,ii] >= modulus:
            nothelpful += 1

    #print nothelpful, "/", BB.dimensions()[0], " vectors are not helpful"

# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii,jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print a

# tries to remove unhelpful vectors
# we start at current = n-1 (last vector)
def remove_unhelpful(BB, monomials, bound, current):
    # end of our recursive function
    if current == -1 or BB.dimensions()[0] <= dimension_min:
        return BB

    # we start by checking from the end
    for ii in range(current, -1, -1):
        # if it is unhelpful:
        if BB[ii, ii] >= bound:
            affected_vectors = 0
            affected_vector_index = 0
            # let's check if it affects other vectors
            for jj in range(ii + 1, BB.dimensions()[0]):
                # if another vector is affected:
                # we increase the count
                if BB[jj, ii] != 0:
                    affected_vectors += 1
                    affected_vector_index = jj

            # level:0
            # if no other vectors end up affected
            # we remove it
            if affected_vectors == 0:
                #print "* removing unhelpful vector", ii
                BB = BB.delete_columns([ii])
                BB = BB.delete_rows([ii])
                monomials.pop(ii)
                BB = remove_unhelpful(BB, monomials, bound, ii-1)
                return BB

            # level:1
            # if just one was affected we check
            # if it is affecting someone else
            elif affected_vectors == 1:
                affected_deeper = True
                for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
                    # if it is affecting even one vector
                    # we give up on this one
                    if BB[kk, affected_vector_index] != 0:
                        affected_deeper = False
                # remove both it if no other vector was affected and
                # this helpful vector is not helpful enough
                # compared to our unhelpful one
                if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(bound - BB[ii, ii]):
                    #print "* removing unhelpful vectors", ii, "and", affected_vector_index
                    BB = BB.delete_columns([affected_vector_index, ii])
                    BB = BB.delete_rows([affected_vector_index, ii])
                    monomials.pop(affected_vector_index)
                    monomials.pop(ii)
                    BB = remove_unhelpful(BB, monomials, bound, ii-1)
                    return BB
    # nothing happened
    return BB

"""
Returns:
* 0,0   if it fails
* -1,-1 if `strict=true`, and determinant doesn't bound
* x0,y0 the solutions of `pol`
"""
def boneh_durfee(pol, modulus, mm, tt, XX, YY):
    """
    Boneh and Durfee revisited by Herrmann and May

    finds a solution if:
    * d < N^delta
    * |x| < e^delta
    * |y| < e^0.5
    whenever delta < 1 - sqrt(2)/2 ~ 0.292
    """

    # substitution (Herrman and May)
    PR.<u, x, y> = PolynomialRing(ZZ)
    Q = PR.quotient(x*y + 1 - u) # u = xy + 1
    polZ = Q(pol).lift()

    UU = XX*YY + 1

    # x-shifts
    gg = []
    for kk in range(mm + 1):
        for ii in range(mm - kk + 1):
            xshift = x^ii * modulus^(mm - kk) * polZ(u, x, y)^kk
            gg.append(xshift)
    gg.sort()

    # x-shifts list of monomials
    monomials = []
    for polynomial in gg:
        for monomial in polynomial.monomials():
            if monomial not in monomials:
                monomials.append(monomial)
    monomials.sort()

    # y-shifts (selected by Herrman and May)
    for jj in range(1, tt + 1):
        for kk in range(floor(mm/tt) * jj, mm + 1):
            yshift = y^jj * polZ(u, x, y)^kk * modulus^(mm - kk)
            yshift = Q(yshift).lift()
            gg.append(yshift) # substitution

    # y-shifts list of monomials
    for jj in range(1, tt + 1):
        for kk in range(floor(mm/tt) * jj, mm + 1):
            monomials.append(u^kk * y^jj)

    # construct lattice B
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
        BB[ii, 0] = gg[ii](0, 0, 0)
        for jj in range(1, ii + 1):
            if monomials[jj] in gg[ii].monomials():
                BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU,XX,YY)

    # Prototype to reduce the lattice
    if helpful_only:
        # automatically remove
        BB = remove_unhelpful(BB, monomials, modulus^mm, nn-1)
        # reset dimension
        nn = BB.dimensions()[0]
        if nn == 0:
            print "failure"
            return 0,0

    # check if vectors are helpful
    if debug:
        helpful_vectors(BB, modulus^mm)

    # check if determinant is correctly bounded
    det = BB.det()
    bound = modulus^(mm*nn)
    if det >= bound:
        #print "We do not have det < bound. Solutions might not be found."
        #print "Try with highers m and t."
        if debug:
            diff = (log(det) - log(bound)) / log(2)
            print "size det(L) - size e^(m*n) = ", floor(diff)
        if strict:
            return -1, -1
    else:
        pass
        #print "det(L) < e^(m*n) (good! If a solution exists < N^delta, it will be found)"

    # display the lattice basis
    if debug:
        matrix_overview(BB, modulus^mm)
    # LLL
    if debug:
        print "optimizing basis of the lattice via LLL, this can take a long time"

    BB = BB.LLL()

    if debug:
        print "LLL is done!"

    # transform vector i & j -> polynomials 1 & 2
    if debug:
        print "looking for independent vectors in the lattice"
    found_polynomials = False

    for pol1_idx in range(nn - 1):
        for pol2_idx in range(pol1_idx + 1, nn):
            # for i and j, create the two polynomials
            PR.<w,z> = PolynomialRing(ZZ)
            pol1 = pol2 = 0
            for jj in range(nn):
                pol1 += monomials[jj](w*z+1,w,z) * BB[pol1_idx, jj] / monomials[jj](UU,XX,YY)
                pol2 += monomials[jj](w*z+1,w,z) * BB[pol2_idx, jj] / monomials[jj](UU,XX,YY)

            # resultant
            PR.<q> = PolynomialRing(ZZ)
            rr = pol1.resultant(pol2)

            # are these good polynomials?
            if rr.is_zero() or rr.monomials() == [1]:
                continue
            else:
                #print "found them, using vectors", pol1_idx, "and", pol2_idx
                found_polynomials = True
                break
        if found_polynomials:
            break

    if not found_polynomials:
        print "no independant vectors could be found. This should very rarely happen..."
        return 0, 0

    rr = rr(q, q)

    # solutions
    soly = rr.roots()

    if len(soly) == 0:
        print "Your prediction (delta) is too small"
        return 0, 0

    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]

    #
    return solx, soly

def dh(N,e,idx):
    # the hypothesis on the private exponent (the theoretical maximum is 0.292)
    delta = .262 # this means that d < N^delta

    #
    # Lattice (tweak those values)
    #

    # you should tweak this (after a first run), (e.g. increment it until a solution is found)
    m = 8 # size of the lattice (bigger the better/slower)

    # you need to be a lattice master to tweak these
    t = int((1-2*delta) * m)  # optimization from Herrmann and May
    X = floor(3*e/N*N^delta) #4*floor(N^delta)  # this _might_ be too much
    Y = floor(2*N^(1/2))    # correct if p, q are ~ same size

    #
    # Don't touch anything below
    #

    # Problem put in equation
    P.<x,y> = PolynomialRing(ZZ)
    A = int((N+1)/2)
    pol = 1 + x * (A + y)

    #
    # Find the solutions!
    #

    # Checking bounds
    if debug:
        print "=== checking values ==="
        print "* delta:", delta
        print "* delta < 0.292", delta < 0.292
        print "* size of e:", int(log(e)/log(2))
        print "* size of N:", int(log(N)/log(2))
        print "* m:", m, ", t:", t

    # boneh_durfee
    if debug:
        print "=== running algorithm ==="
        start_time = time.time()

    solx, soly = boneh_durfee(pol, e, m, t, X, Y)

    # found a solution?
    if solx > 0:
        print "=== solution found ==="
        if False:
            print "x:", solx
            print "y:", soly

        d = int(pol(solx, soly) / e)
        if d>N:
            return 1,0
        print "private key found:", d
        return d,idx
    else:
        pass
        #print "=== no solution was found ==="
    return 1,idx
    if debug:
        print("=== %s seconds ===" % (time.time() - start_time))


def solve():
    data = open('data.txt').read()
    data = data.strip()
    data = data.split('\n')
    possible=literal_eval(data[0])
    nlist =literal_eval(data[1])
    elist = literal_eval(data[2])
#     elist = [
#     120707581153848729541619739304129514317369885703267278333190652065622829839266459618434913605709030828053783733257671342037209489023193158834313382990009754417358925723945002823644472447006088300675953868900288138790896132774308734029600956735020948894668403119284667745513346712464870476283125011032528007603751124322866301885322889992188892699965264667626581746580355375540915633929
# ]
#     d = 2312942448253376880587504992311896441040887226991646614283011019557973340724817418876880506435480396500370416004169
#     nlist = [
#     13839223578712411580229860643907033256028959600963032960703214016782878179186205948935547892804495354976395787885318316974155568871758133400839211683765361230527966678633229577850608540023059600419620116500993374165642140601434351741188206504048346279667593457608209192225058789118181297014713915577238319383465685110547335860915105637862678633086851674123460030194459311425902010548689
# ]
    ans = []
    dlist = []
    for i in range(len(nlist)):
        #raw_input('start i')
        pool = Pool(70)
        n, e = nlist[i], elist[i]
        results=[]
        for j in range(0,125):
            print(i,j)
            tmpe = e * possible[j]
            result = pool.apply_async(dh, args=(int(n),int(tmpe),j))
            results.append(result)
        #pool.close()
        #pool.join()
        cnt = 0
        for i in results:
            i = i.get()
            cnt+=1
            print('cnt=',cnt,'idx = ',i[1])
            if i[0] != 1:
                print 'success',len(dlist)+1
                # raw_input('success one')
                dlist.append(i[0]*possible[i[1]])
                break
        pool.terminate()
        pool.close()
    open('d.txt','w').write(str(dlist))

solve()
