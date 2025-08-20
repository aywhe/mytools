function text = extractext(imgfile)
text = '';
img = imread(imgfile);
head = [9968;123];
text_db = extract_db_(img, length(head)+1);
if any(head - text_db(1:length(head)))
    error('head not match')
end
db_len = text_db(length(head)+1);
if db_len <= 0
    return
end
db_len = db_len + length(head) + 1;
text_db = extract_db_(img, db_len);
text_db = text_db(length(head)+2:end);
text = char(text_db');
end
function text_db = extract_db_(img_in, db_len)
bin_len = db_len * 16;
text_bin = extract_bin_(img_in, bin_len);
text_bin = reshape(text_bin,16,db_len);
text_db = bin2dec(char(text_bin' + '0'));
end
function text_bin = extract_bin_(img_in, bin_len)
loop_sz = numel(img_in);
img_in = permute(img_in,[3 2 1]);
img_out = img_in(:);
text_bin = zeros(bin_len,1);
for b = 1:8
    st = (b-1) * loop_sz + 1;
    if st > length(text_bin)
        break;
    end
    ed = min([b * loop_sz, length(text_bin)]);
    imed = min(loop_sz,ed - st + 1);
    text_bin(st:ed) = bitget(img_out(1:imed),b,'uint8');
end
end