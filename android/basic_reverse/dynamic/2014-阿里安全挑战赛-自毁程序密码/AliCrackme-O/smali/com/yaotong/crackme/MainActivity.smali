.class public Lcom/yaotong/crackme/MainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"


# instance fields
.field public btn_submit:Landroid/widget/Button;

.field public inputCode:Landroid/widget/EditText;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .prologue
    .line 48
    const-string v0, "crackme"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    .line 49
    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 12
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 2
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .prologue
    .line 21
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 22
    const/high16 v0, 0x7f030000

    invoke-virtual {p0, v0}, Lcom/yaotong/crackme/MainActivity;->setContentView(I)V

    .line 23
    invoke-virtual {p0}, Lcom/yaotong/crackme/MainActivity;->getWindow()Landroid/view/Window;

    move-result-object v0

    const/high16 v1, 0x7f020000

    invoke-virtual {v0, v1}, Landroid/view/Window;->setBackgroundDrawableResource(I)V

    .line 25
    const/high16 v0, 0x7f060000

    invoke-virtual {p0, v0}, Lcom/yaotong/crackme/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/EditText;

    iput-object v0, p0, Lcom/yaotong/crackme/MainActivity;->inputCode:Landroid/widget/EditText;

    .line 26
    const v0, 0x7f060001

    invoke-virtual {p0, v0}, Lcom/yaotong/crackme/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lcom/yaotong/crackme/MainActivity;->btn_submit:Landroid/widget/Button;

    .line 28
    iget-object v0, p0, Lcom/yaotong/crackme/MainActivity;->btn_submit:Landroid/widget/Button;

    new-instance v1, Lcom/yaotong/crackme/MainActivity$1;

    invoke-direct {v1, p0}, Lcom/yaotong/crackme/MainActivity$1;-><init>(Lcom/yaotong/crackme/MainActivity;)V

    invoke-virtual {v0, v1}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 44
    return-void
.end method

.method public native securityCheck(Ljava/lang/String;)Z
.end method
