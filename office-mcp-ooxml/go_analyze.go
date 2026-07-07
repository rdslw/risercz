package main

import (
	"fmt"
	"github.com/rcarmo/go-ooxml/pkg/document"
	"github.com/rcarmo/go-ooxml/pkg/spreadsheet"
	"path/filepath"
)

func docx(p string) {
	d, e := document.Open(p)
	if e != nil {
		fmt.Printf("DOCX %s ERROR %v\n", filepath.Base(p), e)
		return
	}
	defer d.Close()
	fmt.Printf("DOCX %s paragraphs=%d tables=%d\n", filepath.Base(p), len(d.Paragraphs()), len(d.Tables()))
	for i, para := range d.Paragraphs() {
		if i < 5 {
			fmt.Printf("  P%d: %s\n", i+1, para.Text())
		}
	}
	for ti, t := range d.Tables() {
		fmt.Printf("  T%d rows=%d cols=%d first=%v\n", ti+1, t.RowCount(), t.ColumnCount(), t.FirstRowText())
	}
}
func xlsx(p string) {
	w, e := spreadsheet.Open(p)
	if e != nil {
		fmt.Printf("XLSX %s ERROR %v\n", filepath.Base(p), e)
		return
	}
	defer w.Close()
	fmt.Printf("XLSX %s sheets=%d tables=%d\n", filepath.Base(p), w.SheetCount(), len(w.Tables()))
	for _, s := range w.Sheets() {
		fmt.Printf("  Sheet %s max=%dx%d A1=%q F9=%q\n", s.Name(), s.MaxRow(), s.MaxColumn(), s.Cell("A1").String(), s.Cell("F9").String())
	}
}
func main() {
	base := "artifacts"
	for _, n := range []string{"python_pl.docx", "go_pl.docx"} {
		docx(filepath.Join(base, n))
	}
	for _, n := range []string{"python_pl.xlsx", "go_pl.xlsx"} {
		xlsx(filepath.Join(base, n))
	}
}
