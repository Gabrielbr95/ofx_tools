from pathlib import Path
import typer
from .loader import load_all_ofx, load_all_txt
from .merger import merge_transactions
from .exporter import export_ofx

app = typer.Typer(help="Ferramenta para processar arquivos OFX e TXT, gerar OFX por usuário.")

DEFAULT_DATA_DIR = Path(__file__).parent.parent.parent / "data"
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"

@app.command()
def run(
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, help="Pasta com arquivos OFX e TXT"),
    output_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, help="Pasta para salvar arquivos OFX gerados")
):
    """Executa o pipeline completo: parse, merge e export."""
    data_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    typer.echo(f"Usando data_dir: {data_dir}")
    typer.echo(f"Usando output_dir: {output_dir}")

    typer.echo("Carregando transações TXT...")
    txt_txs = load_all_txt(data_dir)

    typer.echo("Carregando transações OFX...")
    ofx_txs, acctid_map = load_all_ofx(data_dir)

    typer.echo("Mesclando transações...")
    merged = merge_transactions(ofx_txs, txt_txs)

    typer.echo("Exportando arquivos OFX separados por usuário...")
    export_ofx(merged, data_dir, output_dir, acctid_map)

    typer.echo("Processo concluído!")

if __name__ == "__main__":
    app()
