class noisy_sequence extends uvm_sequence;
  `uvm_object_utils(noisy_sequence)
  `uvm_declare_p_sequencer(my_sequencer)

  function new(string name = "noisy_sequence", uvm_component parent = null);
    super.new(name);
  endfunction

  task body();
    phase.raise_objection(this);
    `uvm_do(req)
    `uvm_do_on(req, p_sequencer)
    `uvm_do_with(req, { addr == 0; })
    `uvm_send(req)
    `uvm_rand_send(req)
    `uvm_create(req)
    req.start(null);
    phase.drop_objection(this);
  endtask
endclass

class noisy_env extends uvm_env;
  `uvm_component_utils(noisy_env)
  `uvm_field_int(counter, UVM_DEFAULT)
  uvm_analysis_imp #(int, noisy_env) item_imp;

  function new(string name = "noisy_env");
    super.new(name);
  endfunction

  function void build_phase(uvm_phase phase);
    uvm_resource_db #(int)::set("scope", "value", 1);
    uvm_config_db #(int)::set(this, "*", "value", 1);
    uvm_config_db #(int)::set(null, "", "value", 1);
    void'(uvm_config_db #(int)::get(this, "", "value", value));
    set_config_int("inst", "field", 1);
    set_config_string("inst", "field", "x");
    set_config_object("inst", "field", cfg);
    get_config_int("field", value);
    get_config_string("field", text);
    get_config_object("field", cfg);
    run_test("hardcoded_test");
    set_global_timeout(0);
    uvm_stop_request();
    global_stop_request();
    uvm_root::get();
    uvm_top.print_topology();
    uvm_report_server::get_server();
  endfunction

  function void connect_phase(uvm_phase phase);
    phase.jump(uvm_run_phase::get());
  endfunction

  task run_phase(uvm_phase phase); endtask

  function void write(int t); endfunction

  task spam();
    for (int i = 0; i < 4; i++) begin
      `uvm_info("LOOP", "loop message", UVM_HIGH)
    end
    `uvm_info("MSG", "always printed", UVM_NONE)
    `uvm_error("ERROR", "generic id")
    `uvm_fatal("FATAL", "generic id")
    $display("display");
    $write("write");
    $strobe("strobe");
    $stop;
    $finish;
  endtask
endclass

class direct_component extends uvm_component;
  function new(string name = "direct_component", uvm_component parent = null);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    noisy_env env;
    env = new("env", this);
    cfg = new("cfg");
    p_sequencer.set_arbitration(UVM_SEQ_ARB_FIFO);
    uvm_config_db #(cfg_t)::set(this, "*", "default_sequence", seq);
    uvm_config_db #(cfg_t)::set(this, "", "agent_cfg", agent_cfg);
  endfunction
endclass
