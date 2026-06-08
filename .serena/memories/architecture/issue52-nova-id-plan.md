# Issue #52 Implementation Plan: `--nova-id` flag for `nodo modifi` and `predikato modifi`

## Overview

Add the ability to rename the primary key of nodes (`node_id`) and predicates (`predicate_id`) via `--nova-id` / `-ni` flag on the existing `modifi` commands. Implemented as separate service methods (`update_node_id`, `update_predicate_id`) — NOT overloading existing `update()`.

