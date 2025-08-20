function encimg(img_infile,img_outfile,text_content)
% embed text in the image
img_in = imread(img_infile);
img_out = encimg_(img_in,text_content);
checkfileext(img_outfile);
imwrite(img_out, img_outfile);
end
function img_out = encimg_(img_in,text)
% embed text in the image
text_bin = enctext_(text);
sz = size(img_in);
if length(sz) < 3
    sz = padarray(sz, [0 3-length(sz)],1, 'post');
end
% calculate data size
if prod(sz)*8 < numel(text_bin)
    error('data size overflow');
end
img_in = permute(img_in,[3 2 1]);
sz2 = size(img_in);
img_out = img_in(:);
loop_sz = prod(sz);
for b = 1:8
    st = (b-1) * loop_sz + 1;
    if st > length(text_bin)
        break;
    end
    ed = min([b * loop_sz, length(text_bin)]);
    imed = min(loop_sz,ed - st + 1);
    img_out(1:imed) = bitset(img_out(1:imed),b,text_bin(st:ed),'uint8');
end
img_out = reshape(img_out,sz2);
img_out = permute(img_out,[3 2 1]);
end
function text_bin = enctext_(text_in)
text_db = double(text_in(:));
head = [9968;123];
text_db = [head; length(text_db); text_db];
text_bin = dec2bin(text_db, 16) - '0';
text_bin = text_bin';
text_bin = text_bin(:);
end
function checkfileext(file)
bad_exts = {'.jpg','.jpeg'};
inds = strfind(file,'.');
if ~isempty(inds)
    ext = file(inds(end):end);
    if ismember(ext,bad_exts)
        error('bad save file extension');
    end
end
end