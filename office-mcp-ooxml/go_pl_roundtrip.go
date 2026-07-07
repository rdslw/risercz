package main

import (
	"fmt"
	"github.com/rcarmo/go-ooxml/pkg/document"
	"github.com/rcarmo/go-ooxml/pkg/spreadsheet"
	"log"
	"os"
	"path/filepath"
)

func main() {
	out := "artifacts"
	os.MkdirAll(out, 0755)
	doc, err := document.New()
	if err != nil {
		log.Fatal(err)
	}
	defer doc.Close()
	doc.AddParagraph().SetText("Acme Cloud Platform P&L FY2026")
	doc.AddParagraph().SetText("Executive summary: revenue expands, gross margin improves, EBITDA turns positive by Q4.")
	t := doc.AddTable(8, 6)
	headers := []string{"Metric", "Q1", "Q2", "Q3", "Q4", "FY"}
	for c, h := range headers {
		t.Cell(0, c).SetText(h)
	}
	rows := [][]string{{"Revenue", "12000000", "13800000", "15500000", "17700000", "59000000"}, {"COGS", "-3840000", "-3864000", "-4185000", "-4779000", "-16668000"}, {"Gross Profit", "8160000", "9936000", "11315000", "12921000", "42332000"}, {"Sales & Marketing", "-4800000", "-5100000", "-5350000", "-5700000", "-20950000"}, {"Product & Engineering", "-3500000", "-3600000", "-3700000", "-3850000", "-14650000"}, {"G&A", "-1300000", "-1350000", "-1400000", "-1420000", "-5470000"}, {"EBITDA", "-1440000", "-114000", "865000", "1951000", "1262000"}}
	for r, row := range rows {
		for c, v := range row {
			t.Cell(r+1, c).SetText(v)
		}
	}
	doc.AddParagraph().SetText("Risk register: enterprise slips, cloud inflation, feature churn; mitigations are commit gates, reserved capacity, and PM conversion scorecards.")
	if err := doc.SaveAs(filepath.Join(out, "go_pl.docx")); err != nil {
		log.Fatal(err)
	}
	wb, err := spreadsheet.New()
	if err != nil {
		log.Fatal(err)
	}
	defer wb.Close()
	sh, _ := wb.Sheet(0)
	sh.SetName("P&L")
	for c, h := range headers {
		sh.CellByRC(1, c+1).SetValue(h)
	}
	for r, row := range rows {
		for c, v := range row {
			sh.CellByRC(r+2, c+1).SetValue(v)
		}
	}
	sh.Cell("A11").SetValue("PM/Sales action")
	sh.Cell("B11").SetValue("Prioritize expansion play + support automation before Q3.")
	sh.AddTable("A1:F8", "PLTable")
	if err := wb.SaveAs(filepath.Join(out, "go_pl.xlsx")); err != nil {
		log.Fatal(err)
	}
	fmt.Println("created go artifacts")
}
