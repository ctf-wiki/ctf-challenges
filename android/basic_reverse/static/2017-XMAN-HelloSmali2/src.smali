.class public Lcom/example/hellosmali/hellosmali/Digest;
.super Ljava/lang/Object;
.source "Digest.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 7
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static check(Ljava/lang/String;)Z
    .locals 14
    .param p0, "input"    # Ljava/lang/String;

    .prologue
    .line 9
    const-string v6, "+/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    .line 11
    .local v6, "str":Ljava/lang/String;
    const/4 v0, 0x6

    .line 12
    .local v0, "a1":I
    const/4 v1, 0x2

    .line 13
    .local v1, "a2":I
    if-eqz p0, :cond_7

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v12

    if-eqz v12, :cond_7

    .line 14
    invoke-virtual {p0}, Ljava/lang/String;->toCharArray()[C

    move-result-object v2

    .line 15
    .local v2, "charinput":[C
    new-instance v8, Ljava/lang/StringBuilder;

    invoke-direct {v8}, Ljava/lang/StringBuilder;-><init>()V

    .line 17
    .local v8, "v2":Ljava/lang/StringBuilder;
    const/4 v3, 0x0

    .local v3, "i":I
    :goto_0
    array-length v12, v2

    if-ge v3, v12, :cond_1

    .line 19
    aget-char v12, v2, v3

    invoke-static {v12}, Ljava/lang/Integer;->toBinaryString(I)Ljava/lang/String;

    move-result-object v4

    .local v4, "intinput":Ljava/lang/String;
    :goto_1
    invoke-virtual {v4}, Ljava/lang/String;->length()I

    move-result v12

    const/16 v13, 0x8

    if-ge v12, v13, :cond_0

    new-instance v12, Ljava/lang/StringBuilder;

    invoke-direct {v12}, Ljava/lang/StringBuilder;-><init>()V

    const-string v13, "0"

    invoke-virtual {v12, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v12

    invoke-virtual {v12, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v12

    invoke-virtual {v12}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    goto :goto_1

    .line 22
    :cond_0
    invoke-virtual {v8, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 17
    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    .line 25
    .end local v4    # "intinput":Ljava/lang/String;
    :cond_1
    :goto_2
    invoke-virtual {v8}, Ljava/lang/StringBuilder;->length()I

    move-result v12

    rem-int/lit8 v12, v12, 0x6

    if-eqz v12, :cond_2

    .line 26
    const-string v12, "0"

    invoke-virtual {v8, v12}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_2

    .line 29
    :cond_2
    invoke-static {v8}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v7

    .line 30
    .local v7, "v1":Ljava/lang/String;
    invoke-virtual {v7}, Ljava/lang/String;->length()I

    move-result v12

    div-int/lit8 v12, v12, 0x6

    new-array v10, v12, [C

    .line 31
    .local v10, "v4":[C
    const/4 v3, 0x0

    :goto_3
    array-length v12, v10

    if-ge v3, v12, :cond_3

    .line 32
    const/4 v12, 0x0

    invoke-virtual {v7, v12, v0}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v12

    invoke-static {v12, v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;I)I

    move-result v11

    .line 33
    .local v11, "v6":I
    invoke-virtual {v7, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v7

    .line 34
    invoke-virtual {v6, v11}, Ljava/lang/String;->charAt(I)C

    move-result v12

    aput-char v12, v10, v3

    .line 31
    add-int/lit8 v3, v3, 0x1

    goto :goto_3

    .line 37
    .end local v11    # "v6":I
    :cond_3
    new-instance v9, Ljava/lang/StringBuilder;

    invoke-static {v10}, Ljava/lang/String;->valueOf([C)Ljava/lang/String;

    move-result-object v12

    invoke-direct {v9, v12}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 38
    .local v9, "v3":Ljava/lang/StringBuilder;
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v12

    rem-int/lit8 v12, v12, 0x3

    const/4 v13, 0x1

    if-ne v12, v13, :cond_5

    .line 39
    const-string v12, "!?"

    invoke-virtual {v9, v12}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 44
    :cond_4
    :goto_4
    invoke-static {v9}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v5

    .line 46
    .local v5, "key":Ljava/lang/String;
    const-string v12, "xsZDluYYreJDyrpDpucZCo!?"

    invoke-virtual {v5, v12}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v12

    if-eqz v12, :cond_6

    .line 47
    const/4 v12, 0x1

    .line 52
    .end local v2    # "charinput":[C
    .end local v3    # "i":I
    .end local v5    # "key":Ljava/lang/String;
    .end local v7    # "v1":Ljava/lang/String;
    .end local v8    # "v2":Ljava/lang/StringBuilder;
    .end local v9    # "v3":Ljava/lang/StringBuilder;
    .end local v10    # "v4":[C
    :goto_5
    return v12

    .line 40
    .restart local v2    # "charinput":[C
    .restart local v3    # "i":I
    .restart local v7    # "v1":Ljava/lang/String;
    .restart local v8    # "v2":Ljava/lang/StringBuilder;
    .restart local v9    # "v3":Ljava/lang/StringBuilder;
    .restart local v10    # "v4":[C
    :cond_5
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v12

    rem-int/lit8 v12, v12, 0x3

    if-ne v12, v1, :cond_4

    .line 41
    const-string v12, "!"

    invoke-virtual {v9, v12}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_4

    .line 49
    .restart local v5    # "key":Ljava/lang/String;
    :cond_6
    const/4 v12, 0x0

    goto :goto_5

    .line 52
    .end local v2    # "charinput":[C
    .end local v3    # "i":I
    .end local v5    # "key":Ljava/lang/String;
    .end local v7    # "v1":Ljava/lang/String;
    .end local v8    # "v2":Ljava/lang/StringBuilder;
    .end local v9    # "v3":Ljava/lang/StringBuilder;
    .end local v10    # "v4":[C
    :cond_7
    const/4 v12, 0x0

    goto :goto_5
.end method
