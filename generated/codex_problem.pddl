(define (problem codexproblem) (:domain Codex)
(:objects
	depot0 - Depot
	distributor0 distributor1 - Distributor
	truck0 truck1 - Truck
	pallet0 pallet1 pallet2 - Pallet
	crate0 crate1 - Crate
	hoist0 hoist1 hoist2 - Hoist)
(:init
(at truck0 depot1))
(:goal (and (on crate0 pallet0) (on crate1 pallet1)))
)