from pathlib import Path
from datetime import datetime
import torch
import gradio as gr
from idol import IdolPipeline

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
PIPELINE = None

def get_pipeline():
    global PIPELINE
    if PIPELINE is None:
        PIPELINE = IdolPipeline.from_pretrained("speridlabs/idol")
    return PIPELINE

def gerar(imagem, modo, gaussians, seed, progresso=gr.Progress()):
    if not imagem:
        raise gr.Error("Envie uma imagem antes de gerar.")
    if not torch.cuda.is_available():
        raise gr.Error("CUDA/GPU NVIDIA não detectada. Confira o driver e o PyTorch CUDA.")
    try:
        progresso(0.05, desc="Carregando o modelo Idol...")
        pipe = get_pipeline()
        progresso(0.15, desc="Gerando modelo 3D...")
        resultado = pipe(imagem, mode=modo, seed=int(seed), num_gaussians=int(gaussians))
        nome = Path(imagem).stem
        destino = OUT / f"{nome}_{datetime.now():%Y%m%d_%H%M%S}.ply"
        resultado.gaussian.save_ply(str(destino))
        progresso(1, desc="Concluído!")
        return str(destino), f"Modelo salvo: {destino.name}\nGaussians: {int(gaussians):,}\nGPU: {torch.cuda.get_device_name(0)}"
    except Exception as exc:
        raise gr.Error(f"Falha na geração: {exc}") from exc

def listar_historico():
    arquivos = sorted(OUT.glob("*.ply"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [[p.name, f"{p.stat().st_size / (1024*1024):.1f} MB", datetime.fromtimestamp(p.stat().st_mtime).strftime("%d/%m/%Y %H:%M")] for p in arquivos[:30]]

def status():
    if torch.cuda.is_available():
        return f"GPU detectada: {torch.cuda.get_device_name(0)} | CUDA {torch.version.cuda}"
    return "GPU NVIDIA não detectada. Verifique o PyTorch CUDA."

with gr.Blocks(title="3DME — Idol Studio", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 3DME — Idol Studio\nTransforme uma imagem em um modelo 3D Gaussian Splat (.PLY), localmente no seu computador.")
    gr.Markdown("### Estado do sistema")
    gr.Markdown(f"**{status()}**")
    with gr.Row():
        with gr.Column(scale=1):
            imagem = gr.Image(label="Imagem de entrada", type="filepath", sources=["upload"], height=360)
            modo = gr.Radio(choices=[("Imagem/render 3D", "synthetic"), ("Fotografia real", "real")], value="synthetic", label="Tipo de imagem")
            gaussians = gr.Dropdown(choices=[32768, 65536, 131072, 262144, 524288, 1048576], value=262144, label="Quantidade de Gaussians")
            seed = gr.Number(value=42, precision=0, label="Seed")
            gerar_btn = gr.Button("GERAR MODELO 3D", variant="primary")
        with gr.Column(scale=1):
            arquivo = gr.File(label="Baixar modelo 3D (.PLY)")
            resultado = gr.Textbox(label="Resultado", lines=4)
            gr.Markdown("**Dica:** comece com 65.536 ou 131.072 Gaussians se sua GPU tiver pouca VRAM.")
    gerar_btn.click(gerar, inputs=[imagem, modo, gaussians, seed], outputs=[arquivo, resultado])
    gr.Markdown("### Histórico local")
    historico = gr.Dataframe(headers=["Arquivo", "Tamanho", "Data"], datatype=["str", "str", "str"], value=listar_historico, interactive=False)
    atualizar = gr.Button("Atualizar histórico")
    atualizar.click(listar_historico, outputs=historico)
    gr.Markdown("Os arquivos são armazenados em outputs. A interface escuta somente em localhost.")

if __name__ == "__main__":
    demo.queue().launch(server_name="127.0.0.1", server_port=7860, share=False, inbrowser=True)
