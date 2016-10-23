module tb_ssd1306_8x64bit_driver;

reg clk;
reg reset;
wire reset_out;
reg [63:0] val0;
reg [63:0] val1;
reg [63:0] val2;
reg [63:0] val3;
reg [63:0] val4;
reg [63:0] val5;
reg [63:0] val6;
reg [63:0] val7;
reg [7:0] control_contrast;
reg control_inversion;
wire spi_csn;
wire spi_clk;
wire spi_dcn;
wire spi_mosi;

initial begin
    $from_myhdl(
        clk,
        reset,
        val0,
        val1,
        val2,
        val3,
        val4,
        val5,
        val6,
        val7,
        control_contrast,
        control_inversion
    );
    $to_myhdl(
        reset_out,
        spi_csn,
        spi_clk,
        spi_dcn,
        spi_mosi
    );
end

ssd1306_8x64bit_driver dut(
    clk,
    reset,
    reset_out,
    val0,
    val1,
    val2,
    val3,
    val4,
    val5,
    val6,
    val7,
    control_contrast,
    control_inversion,
    spi_csn,
    spi_clk,
    spi_dcn,
    spi_mosi
);

endmodule
