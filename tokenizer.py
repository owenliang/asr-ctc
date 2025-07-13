import json 
import re 

class Tokenizer:
    def __init__(self,special_tokens=[]):
        self.chr_to_id={}
        self.id_to_chr={}
        self.special_tokens=special_tokens
        for token in special_tokens:
            self._insert_token(token)
    
    def _insert_token(self,chr):
        if chr not in self.chr_to_id:
            self.chr_to_id[chr]=len(self.chr_to_id)
            self.id_to_chr[self.chr_to_id[chr]]=chr
        
    def train_from_iterator(self,iterator):
        for i,text in enumerate(iterator):
            for chr in text:
                self._insert_token(chr)
            if i%10000==0:
                print(f'training tokenizer... {i}')
    def encode(self, text):
        pattern='('+'|'.join([re.escape(tok) for tok in self.special_tokens])+')'
        splits=re.split(pattern,text)
        
        token_ids=[]
        for sub_text in splits:
            if sub_text in self.special_tokens: 
                token_ids.append(self.chr_to_id[sub_text])
            else:
                for chr in sub_text:
                    token_ids.append(self.chr_to_id[chr])
        return token_ids
    
    def decode(self,token_ids):
        # 相邻重复token合并
        token_ids_merged=[]
        for token_id in token_ids:
            token_id=token_id
            if len(token_ids_merged) and token_id==token_ids_merged[-1]:
                continue 
            token_ids_merged.append(token_id)
        
        tokens=[]
        for token_id in token_ids_merged:
            token=self.id_to_chr[token_id]
            if token in self.special_tokens:
                continue
            tokens.append(token)
        return ''.join(tokens)
    
    def get_vocab_size(self):
        return len(self.chr_to_id)
    
    def save(self,filename):
        with open(filename,'w') as fp:
            json.dump({'chr_to_id':self.chr_to_id,'special_tokens':self.special_tokens},fp)
    
    @staticmethod
    def from_file(filename):
        tokenizer=Tokenizer()
        with open(filename,'r') as fp:
            data=json.load(fp)
            tokenizer.chr_to_id=data['chr_to_id']
            tokenizer.id_to_chr={id:chr for chr,id in tokenizer.chr_to_id.items()}
            tokenizer.special_tokens=data['special_tokens']
        return tokenizer
    
if __name__=='__main__':
    tokenizer=Tokenizer.from_file('tokenizer.json')
    token_ids=tokenizer.encode('HELLO[BLANK] WORLD')
    print(token_ids)
    print(tokenizer.decode(token_ids))