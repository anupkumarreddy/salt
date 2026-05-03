`timescale 1ns/1ps
`include "legacy_defs.svh"
`define LOCAL_WIDTH 8
import shared_pkg::*;

program legacy_program;
endprogram

module community_sv_violations #(WIDTH = 8) (
  input logic clk,
  input logic rst_n,
  output logic done
);
  wire legacy_net;
  reg [3:0] legacy_reg;
  parameter DEPTH = 16;
  localparam LIMIT = 4;
  logic initialized = 1'b0;
  real gain;
  realtime stamp;
  shortreal ratio;
  event sample_ev;
  mailbox mbx;
  semaphore sem;
  process proc;
  tri internal_bus;

  defparam u_child.DEPTH = 4;

  child #(.WIDTH(WIDTH)) u_named (.clk(clk));
  child #(WIDTH) u_positional (.clk(clk));
  child #(8, 4) u_positional2 (.clk(clk));
  child u_wild (.*);
  wire (strong1, weak0) strength_net;

  initial begin
    begin
    end
    force done = 1'b1;
    release done;
    deassign done;
    wait (done);
    wait fork;
    disable fork;
    disable legacy_block;
    #10 legacy_task();
    #5;
    legacy_reg++;
    legacy_reg = 4'bxxxx;
    legacy_reg = 4'bzzzz;
    legacy_reg.randomize();
    -> sample_ev;
  end

  always_latch begin
    if (rst_n) done = 1'b1;
  end

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) done <= 1'b0;
    else done <= legacy_net;
  end

  always @ (clk, rst_n) begin
    done = clk;
  end

  casez (legacy_reg)
    4'b1???: done = 1'b1;
    default: done = 1'b0;
  endcase
  full_case parallel_case;

  `translate_off
  randcase
    1: done = 1'b1;
  endcase
  `translate_on

  randsequence(seq)
    seq: {};
  endsequence

  fork
    legacy_task();
  join_none

  final begin
    $display("done");
  end

  expect (done);

endmodule

module child #(parameter int WIDTH = 1, parameter int DEPTH = 1) (
  input logic clk
);
endmodule
