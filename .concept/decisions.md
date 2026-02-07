# Active AUTO Decisions (cache) — safe to delete

*AUTO-GENERATED from ontology.yml.assumptions and ambiguities.yml.auto_decision*
*Last updated: 2026-02-08T02:20:00Z (cycle-005)*

## ASM-001: Term Queue Flow
- **Decision Key**: CONCEPT_SYNC:term_queue_flow
- **Status**: ACTIVE
- **Chosen**: New canonical terms must go through term_queue.yml for review before being added to ontology
- **Policy**: bloat_control + process_consistency
- **Expires After Runs**: 50
- **Linked Term**: TermQueue
- **Revert Triggers**: primary_evidence_contradiction, security_risk

## ASM-002: Decisions Cache
- **Decision Key**: CONCEPT_SYNC:decisions_cache
- **Status**: ACTIVE
- **Chosen**: decisions.md is a cache file with 200 line limit. Source of truth is ambiguities.yml.auto_decision
- **Policy**: bloat_control + cache_management
- **Expires After Runs**: 50
- **Linked Term**: DecisionsCache
- **Revert Triggers**: primary_evidence_contradiction, system_redesign

## ASM-003: Immutable AD Model
- **Decision Key**: CONSTITUTION:immutable_AD_model
- **Status**: ACTIVE
- **Chosen**: A-D状態遷移モデルはSYSTEM_CONSTITUTION.md 2.1で定義されており、変更してはならない
- **Policy**: constitution_invariant
- **Expires After Runs**: 999
- **Linked Term**: ADStateModel
- **Revert Triggers**: constitution_amendment

---

*This file is a cache. The truth is in ambiguities.yml.auto_decision and ontology.yml.assumptions*
*Limit: 200 lines. Regenerate from source if exceeded.*
