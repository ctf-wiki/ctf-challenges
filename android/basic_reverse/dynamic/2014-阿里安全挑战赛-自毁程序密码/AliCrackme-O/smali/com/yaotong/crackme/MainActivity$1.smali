.class Lcom/yaotong/crackme/MainActivity$1;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/yaotong/crackme/MainActivity;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/yaotong/crackme/MainActivity;


# direct methods
.method constructor <init>(Lcom/yaotong/crackme/MainActivity;)V
    .locals 0

    .prologue
    .line 1
    iput-object p1, p0, Lcom/yaotong/crackme/MainActivity$1;->this$0:Lcom/yaotong/crackme/MainActivity;

    .line 28
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 5
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 33
    iget-object v2, p0, Lcom/yaotong/crackme/MainActivity$1;->this$0:Lcom/yaotong/crackme/MainActivity;

    iget-object v2, v2, Lcom/yaotong/crackme/MainActivity;->inputCode:Landroid/widget/EditText;

    invoke-virtual {v2}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    move-result-object v2

    invoke-interface {v2}, Landroid/text/Editable;->toString()Ljava/lang/String;

    move-result-object v1

    .line 34
    .local v1, "result":Ljava/lang/String;
    iget-object v2, p0, Lcom/yaotong/crackme/MainActivity$1;->this$0:Lcom/yaotong/crackme/MainActivity;

    invoke-virtual {v2, v1}, Lcom/yaotong/crackme/MainActivity;->securityCheck(Ljava/lang/String;)Z

    move-result v2

    if-eqz v2, :cond_0

    .line 35
    new-instance v0, Landroid/content/Intent;

    iget-object v2, p0, Lcom/yaotong/crackme/MainActivity$1;->this$0:Lcom/yaotong/crackme/MainActivity;

    const-class v3, Lcom/yaotong/crackme/ResultActivity;

    invoke-direct {v0, v2, v3}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 36
    .local v0, "i":Landroid/content/Intent;
    iget-object v2, p0, Lcom/yaotong/crackme/MainActivity$1;->this$0:Lcom/yaotong/crackme/MainActivity;

    invoke-virtual {v2, v0}, Lcom/yaotong/crackme/MainActivity;->startActivity(Landroid/content/Intent;)V

    .line 42
    .end local v0    # "i":Landroid/content/Intent;
    :goto_0
    return-void

    .line 39
    :cond_0
    iget-object v2, p0, Lcom/yaotong/crackme/MainActivity$1;->this$0:Lcom/yaotong/crackme/MainActivity;

    invoke-virtual {v2}, Lcom/yaotong/crackme/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v2

    const-string v3, "\u9a8c\u8bc1\u7801\u6821\u9a8c\u5931\u8d25"

    .line 40
    const/4 v4, 0x0

    .line 39
    invoke-static {v2, v3, v4}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v2

    .line 40
    invoke-virtual {v2}, Landroid/widget/Toast;->show()V

    goto :goto_0
.end method
