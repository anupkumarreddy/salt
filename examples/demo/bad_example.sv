module BadModule;
	logic a;    

always_ff @(posedge clk) begin
  a = 1'b1;
end

always_comb begin
  a <= 1'b0;
end

casex (sel)
  2'b00: a = 1'b0;
endcase

endmodule
