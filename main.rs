// OPTIMIZE THIS FUNCTION TO RUN AS FAST AS POSSIBLE
// Result must work on play.rust-lang.org

/// Returns the 8 smallest numbers found in the supplied vector
/// in order smallest to largest.
fn least_8(l: &Vec<u32>) -> Vec<u32> {
    let mut result_vec = vec![l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7]];
    result_vec.sort();
    let mut max_element = result_vec.pop().unwrap();
    for element in &l[8..] {
        if element < &max_element {
            if element > &result_vec[6] {
                max_element = *element;
                continue;
            }
            let exact_idx = result_vec.partition_point(|&x| x < *element);
            result_vec.insert(exact_idx, *element);
            max_element = result_vec.pop().unwrap();
        }
    }
    result_vec.insert(7, max_element);
    result_vec
}

// DO NOT CHANGE ANYTHING BELOW THIS LINE

fn make_list() -> Vec<u32> {
    const SIZE: usize = 1 << 16;
    let mut out = Vec::with_capacity(SIZE);
    let mut num = 998_244_353_u32; // prime
    for i in 0..SIZE {
        out.push(num);
        // rotate and add to produce some pseudorandomness
        num = (((num << 1) | (num >> 31)) as u64 + (i as u64)) as u32;
    }
    return out;
}

fn main() {
    let l = make_list();
    let start = std::time::Instant::now();
    let l8 = least_8(&l);
    let end = std::time::Instant::now();
    assert_eq!(vec![4, 5, 15, 22, 28, 31, 37, 38], l8);
    println!("Took {:?}", end.duration_since(start));
}

