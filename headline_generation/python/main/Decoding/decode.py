
D = []#List of words from news aritcle
P = []#POS for the news article
T = 0 #number of top scoring headlines to be returned
ML = 0 #Max length of headline to be returned
C1 = 0#beam search cut off value
C2 = 0#C1,C2 > T(C1>C2)
W_vb = []#initial word translation set
alpha = [] #content selection parameter list 
lmda = [] #headline synthesis para-meter list
P_wt = []
P_lm = []
P_pos_lm = []

def top_T_headlines():
#Initialize prioity_queue
	S = S_f = Queue.PriorityQueue()
	D_v = Calculate_Word_Translation_Set(D, L, W_vb, P, P_wt)
	for m in range(0,C1):
		h_m = ["start"]
		# Initial sequence is empty and sequence score is 0
		S.put(h_m,0)

	for i in range(0,ML):
		# Set correct value of cut-off (no of increments)
		if i<=5: # <=5 for C1, 5< for C2
			M = C1
		else:
			M = C2

		for m in range(0,M):
			# Decoding Step: Only the top C1 (C2 ) sequences are retained and expanded
			h,s = S.get()

			for l in range(0,L):
				h_add = W_vb[l]#######check this statement
				s = PWS(h_add)
				Sf.put(h_add,s)

			for j in range(0,V):### check for V
				h_add = V[j]#######check this statement 
				s = PWS(h_add)
				Sf.put(h_add,s)
		# Set S to Sf , and Reset Sf for new search iteration
		S = Sf
		Sf = []
		Display_Top_Headlines(S,T)


def Calculate_Word_Translation_Set(D, L, W_vb, P, P_wt):;
	D_v = []
	V = len(W_vb)
	for l in range(0,L):
		#only for words with pos verb forms
		if P[l] == "VB":
			for i in range(0,V):
				if P_wt[W_vb[i]][D[l]] > 0:
					# Extract word translation substitution set
					D_v = D_v.append(W_vb[i])

	return D_v

def Display_Top_Headlines(S,T):
	# Output Top T Headlines
	for i in range(1,T):
		h,p = S.get() #get headline h and priority p
		print h,p


def main()
	
	top_T_headlines(D, L, W_vb, P, P_wt)





if __name__ == "__main__":
    main()
