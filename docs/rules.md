# SALT Rule Reference

This document lists the community guideline rules added for SystemVerilog and UVM. These rules are intentionally lightweight checks backed by SALT's comment-stripped scanner; they catch common patterns but do not replace compiler, elaboration, or formal lint checks.

## SystemVerilog Community Rules

| ID | Rule | Guideline |
| --- | --- | --- |
| SV005 | `no_defparam` | Use instance parameter overrides instead of `defparam`. |
| SV006 | `no_wildcard_import` | Import explicit package symbols instead of wildcard imports. |
| SV007 | `no_wildcard_port_connection` | Use explicit named port connections instead of `.*`. |
| SV008 | `no_force_statement` | Avoid `force` in checked code. |
| SV009 | `no_release_statement` | Avoid `release` in checked code. |
| SV010 | `no_wait_statement` | Prefer event controls, clocking blocks, or bounded waits over `wait()`. |
| SV011 | `no_join_none` | Avoid unmanaged process lifetimes from `join_none`. |
| SV012 | `no_disable_fork` | Avoid `disable fork`; keep process ownership explicit. |
| SV013 | `no_deassign_statement` | Avoid legacy procedural continuous assignment cleanup with `deassign`. |
| SV014 | `no_drive_strength` | Avoid drive strength annotations in portable source. |
| SV015 | `no_internal_tristate_net` | Prefer muxed logic over internal tri-state nets. |
| SV016 | `no_casez` | Avoid `casez` wildcard matching unless specifically reviewed. |
| SV017 | `no_full_case_parallel_case` | Use language semantics instead of `full_case` or `parallel_case` pragmas. |
| SV018 | `no_translate_off` | Isolate simulation-only code instead of inline `translate_off` regions. |
| SV019 | `no_mixed_edge_event_control` | Do not mix posedge and negedge controls in the same event expression. |
| SV020 | `no_always_latch` | Avoid intentional latch blocks unless required by design intent. |
| SV021 | `no_x_assignment` | Avoid assigning unknown (`X`) values in checked source. |
| SV022 | `no_z_assignment` | Avoid assigning high-impedance (`Z`) values except at IO boundaries. |
| SV023 | `no_real_type` | Avoid `real` variables in portable linted source. |
| SV024 | `no_realtime_type` | Avoid `realtime` variables in portable linted source. |
| SV025 | `no_shortreal_type` | Avoid `shortreal` variables in portable linted source. |
| SV026 | `no_event_variable` | Prefer typed synchronization mechanisms over raw `event` variables. |
| SV027 | `no_mailbox` | Prefer typed FIFOs or UVM TLM channels over `mailbox`. |
| SV028 | `no_semaphore` | Prefer explicit ownership protocols over `semaphore`. |
| SV029 | `no_process_class` | Avoid direct `process` handle manipulation unless reviewed. |
| SV030 | `no_randomize_in_rtl` | Keep `.randomize()` calls in controlled verification code. |
| SV031 | `no_randcase` | Prefer explicit constrained-random stimulus over `randcase`. |
| SV032 | `no_randsequence` | Prefer explicit sequence objects or constrained-random code over `randsequence`. |
| SV033 | `no_program_block` | Use modules, interfaces, packages, and classes instead of `program`. |
| SV034 | `no_implicit_event_or` | Avoid comma-separated event controls. |
| SV035 | `no_unnamed_begin` | Name nontrivial `begin` blocks for traceability. |
| SV036 | `no_unnamed_fork` | Name `fork` blocks when process control or debug visibility matters. |
| SV037 | `no_positional_parameter_override` | Use named parameter overrides. |
| SV038 | `no_positional_task_call_delay` | Avoid fixed delays before task calls. |
| SV039 | `no_hash_delay` | Avoid arbitrary `#` delays in linted source. |
| SV040 | `no_disable_statement` | Prefer structured control flow over `disable`. |
| SV041 | `no_wait_fork` | Avoid `wait fork`; make joins explicit. |
| SV042 | `no_expect_statement` | Prefer assertions or explicit checks over `expect`. |
| SV043 | `no_final_block` | Prefer explicit end-of-test reporting over `final` blocks. |
| SV044 | `no_inc_dec_in_expression` | Use explicit assignments instead of `++` or `--` when clarity matters. |
| SV045 | `no_macro_definition_in_source` | Centralize macros rather than defining them locally. |
| SV046 | `no_include_in_source` | Prefer packages and compilation units over textual includes. |
| SV047 | `no_timescale_in_source` | Prefer `timeunit` and `timeprecision` over `` `timescale``. |
| SV048 | `no_untyped_parameter` | Declare parameter types explicitly. |
| SV049 | `no_untyped_localparam` | Declare localparam types explicitly. |
| SV050 | `no_legacy_reg` | Use `logic` instead of legacy `reg`. |
| SV051 | `no_legacy_wire_for_variables` | Use `logic` for internal variables unless net semantics are required. |
| SV052 | `no_assign_in_declaration` | Initialize state in reset logic or constructors, not declarations. |
| SV053 | `require_default_nettype_none` | Add `` `default_nettype none`` to files that declare modules. |
| SV054 | `require_timeunit_timeprecision` | Declare `timeunit` and `timeprecision` in files that declare modules. |

## UVM Community Rules

| ID | Rule | Guideline |
| --- | --- | --- |
| UVM003 | `uvm_no_do_macro` | Prefer explicit create/start/randomize flow over `` `uvm_do``. |
| UVM004 | `uvm_no_do_on_macro` | Prefer explicit sequencer targeting over `` `uvm_do_on``. |
| UVM005 | `uvm_no_do_with_macro` | Prefer explicit randomize constraints over `` `uvm_do_with``. |
| UVM006 | `uvm_no_send_macro` | Prefer explicit item or sequence flow over `` `uvm_send``. |
| UVM007 | `uvm_no_rand_send_macro` | Prefer explicit randomize and send flow over `` `uvm_rand_send``. |
| UVM008 | `uvm_no_create_macro` | Prefer `type_id::create` over `` `uvm_create``. |
| UVM009 | `uvm_no_resource_db` | Prefer `uvm_config_db` over `uvm_resource_db`. |
| UVM010 | `uvm_no_config_db_wildcard_set` | Avoid wildcard paths in `uvm_config_db::set`. |
| UVM011 | `uvm_no_config_db_null_context` | Use a component context for `uvm_config_db` access. |
| UVM012 | `uvm_no_set_config_int` | Replace legacy `set_config_int` with `uvm_config_db`. |
| UVM013 | `uvm_no_set_config_string` | Replace legacy `set_config_string` with `uvm_config_db`. |
| UVM014 | `uvm_no_set_config_object` | Replace legacy `set_config_object` with `uvm_config_db`. |
| UVM015 | `uvm_no_get_config_int` | Replace legacy `get_config_int` with `uvm_config_db`. |
| UVM016 | `uvm_no_get_config_string` | Replace legacy `get_config_string` with `uvm_config_db`. |
| UVM017 | `uvm_no_get_config_object` | Replace legacy `get_config_object` with `uvm_config_db`. |
| UVM018 | `uvm_no_global_timeout_zero` | Do not disable UVM timeout with zero. |
| UVM019 | `uvm_no_stop_request` | Use phase objections instead of deprecated `uvm_stop_request`. |
| UVM020 | `uvm_no_global_stop_request` | Use phase objections instead of global stop request APIs. |
| UVM021 | `uvm_no_objection_in_sequence` | Keep objections in components or tests, not sequences. |
| UVM022 | `uvm_no_phase_jump` | Avoid phase jumps in normal test flow. |
| UVM023 | `uvm_no_direct_root_access` | Avoid direct `uvm_root::get` coordination. |
| UVM024 | `uvm_no_top_access` | Avoid global `uvm_top` access in regular testbench code. |
| UVM025 | `uvm_no_report_server_global` | Prefer scoped report APIs over global report server mutation. |
| UVM026 | `uvm_no_display` | Use UVM reporting instead of `$display`. |
| UVM027 | `uvm_no_write` | Use UVM reporting instead of `$write`. |
| UVM028 | `uvm_no_strobe` | Use UVM reporting instead of `$strobe`. |
| UVM029 | `uvm_no_finish` | End tests with objections and phase completion instead of `$finish`. |
| UVM030 | `uvm_no_stop` | Use controlled UVM shutdown instead of `$stop`. |
| UVM031 | `uvm_no_fatal_without_id` | Use specific IDs for `` `uvm_fatal`` messages. |
| UVM032 | `uvm_no_error_without_id` | Use specific IDs for `` `uvm_error`` messages. |
| UVM033 | `uvm_no_info_none` | Use an intentional verbosity instead of `UVM_NONE` for info messages. |
| UVM034 | `uvm_no_info_high_in_loops` | Avoid unthrottled `` `uvm_info`` calls in loops. |
| UVM035 | `uvm_no_component_new_without_parent` | Component constructors should accept `name` and `parent`. |
| UVM036 | `uvm_no_object_new_with_parent` | Object constructors should not take a component parent. |
| UVM037 | `uvm_no_direct_component_new` | Create components through the factory. |
| UVM038 | `uvm_no_direct_object_new` | Create UVM objects through the factory unless bypassing it is intentional. |
| UVM039 | `uvm_no_missing_super_build` | Call `super.build_phase(phase)` when overriding build phase. |
| UVM040 | `uvm_no_missing_super_connect` | Call `super.connect_phase(phase)` when overriding connect phase. |
| UVM041 | `uvm_no_missing_super_run` | Call `super.run_phase(phase)` when overriding run phase. |
| UVM042 | `uvm_no_get_without_check` | Check the return value of `uvm_config_db::get`. |
| UVM043 | `uvm_no_analysis_imp_write_empty` | Implement or remove empty analysis `write` methods. |
| UVM044 | `uvm_no_sequence_start_null` | Start sequences on explicit sequencers. |
| UVM045 | `uvm_no_sequencer_arbitration_fifo` | Avoid hard-coded FIFO arbitration unless required. |
| UVM046 | `uvm_no_default_sequence` | Prefer explicit virtual sequence starts over `default_sequence`. |
| UVM047 | `uvm_no_p_sequencer_macro` | Prefer explicit sequencer handles over `` `uvm_declare_p_sequencer``. |
| UVM048 | `uvm_no_field_automation` | Prefer intentional `do_copy`, `do_compare`, and `do_print` implementations over field macros. |
| UVM049 | `uvm_no_config_object_clone_zero` | Clone mutable config objects before sharing through `config_db`. |
| UVM050 | `uvm_no_hardcoded_testname` | Pass test names from the simulator command line. |
| UVM051 | `uvm_no_empty_run_phase` | Remove empty `run_phase` overrides. |
| UVM052 | `uvm_no_missing_factory_create` | Use `type_id::create` in files that declare UVM classes. |

## HTML Reporting

Generate an HTML report with:

```bash
salt check <path> --format html > salt-report.html
```

The HTML report includes total counts, severity counts, and a scan-friendly table with file, line, column, severity, rule ID, rule name, and message.
