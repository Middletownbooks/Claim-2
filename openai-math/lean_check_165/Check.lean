import OAI.Combinatorics.Crossing.Main

#print axioms OAI.Zarankiewicz.mainTarget_proof
#check @OAI.Zarankiewicz.mainTarget_proof
#print OAI.Zarankiewicz.MainTarget
-- the instance this repository's v4 thread works: cr(K_{7,11})
example : OAI.Zarankiewicz.axisPairs 7 * OAI.Zarankiewicz.axisPairs 11 = 225 := by decide
#print axioms OAI.Zarankiewicz.ordinary_crossing_number_eq
